from flask import Flask, request, jsonify
import re
import time
import requests

app = Flask(__name__)

banco_dados_seguro = []
controle_ips = {}
tentativas_login = {}

MAX_PAYLOAD_SIZE = 1024
MAX_REQUISICOES_POR_MINUTO = 10

# --- FIREWALL DINAMICO E RASTREAMENTO ---
BLACKLIST = set()

def rastrear_origem_ip(ip):
    if ip == "127.0.0.1": 
        return "Localhost (Teste Interno)"
    try:
        resposta = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
        if resposta.get("status") == "success":
            return f"{resposta.get('city')}, {resposta.get('country')}"
    except:
        pass
    return "Localizacao Desconhecida"

def sanitizar_entrada(texto):
    if not isinstance(texto, str): return texto
    return re.sub(r'[<>\$;\']', '', texto)

def verificar_rate_limit(ip_cliente):
    tempo_atual = time.time()
    if ip_cliente not in controle_ips:
        controle_ips[ip_cliente] = []
    controle_ips[ip_cliente] = [t for t in controle_ips[ip_cliente] if tempo_atual - t < 60]
    
    if len(controle_ips[ip_cliente]) >= MAX_REQUISICOES_POR_MINUTO:
        return False
    controle_ips[ip_cliente].append(tempo_atual)
    return True

@app.route('/postgres/v1/authenticate', methods=['POST'])
def armadilha_login_falso():
    ip_origem = request.remote_addr
    
    # 0. REGRA DE FIREWALL: Bloqueio imediato
    if ip_origem in BLACKLIST:
        print(f"[FIREWALL] Bloqueio automatico executado para o IP: {ip_origem}")
        return jsonify({"error": "Acesso negado pelo Firewall. IP Banido."}), 403
    
    if not verificar_rate_limit(ip_origem):
        return jsonify({"error": "Connection reset by peer"}), 429
    if request.content_length and request.content_length > MAX_PAYLOAD_SIZE:
        return jsonify({"error": "Payload too large"}), 413

    # 1. RASTREAMENTO E ALERTA
    localizacao = rastrear_origem_ip(ip_origem)
    dados_recebidos = request.get_json(silent=True) or {}
    
    log_auditoria = {
        "timestamp": time.ctime(),
        "ip_atacante": ip_origem,
        "origem": localizacao,
        "acao": "Tentativa de Forca Bruta",
        "payload_enviado": {k: sanitizar_entrada(str(v)) for k, v in dados_recebidos.items()}
    }
    banco_dados_seguro.append(log_auditoria)
    print(f"\n[ALERTA SILENCIOSO] Hacker de {localizacao} ({ip_origem}) detectado!")

    time.sleep(3) 

    tentativas_login[ip_origem] = tentativas_login.get(ip_origem, 0) + 1
    
    if tentativas_login[ip_origem] >= 3 or dados_recebidos.get("password") == "admin123":
        
        # 2. ADICIONA À BLACKLIST APÓS CAIR NA ARMADILHA
        if tentativas_login[ip_origem] >= 3:
            BLACKLIST.add(ip_origem)
            print(f"[FIREWALL] IP {ip_origem} adicionado a Blacklist permanentemente.")
            
        return jsonify({
            "status": "Autenticado com Sucesso",
            "db_version": "PostgreSQL 14.2",
            "tabelas_disponiveis": [
                "tb_folha_pagamento_2024",
                "tb_cartoes_credito_clientes",
                "tb_senhas_diretoria"
            ],
            "mensagem": "Bem-vindo ao banco de dados principal."
        }), 200
    else:
        return jsonify({"error": "Authentication failed for user"}), 401

if __name__ == '__main__':
    print("=== HONEYDB TARPIT & FIREWALL INICIADO ===")
    app.run(host='0.0.0.0', port=5000)
