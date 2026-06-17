from flask import Flask, request, jsonify
import re
import time

app = Flask(__name__)

# --- CAIXA PRETA: Onde os logs do hacker são guardados de verdade ---
banco_dados_seguro = []
controle_ips = {} # Memória para o Rate Limiting
tentativas_login = {} # Memória para simular a falha e o sucesso falso

# --- CONFIGURAÇÕES DE SEGURANÇA (As 3 Mitigações de Software) ---
MAX_PAYLOAD_SIZE = 1024 # Evita Buffer Overflow (Max 1KB)
MAX_REQUISICOES_POR_MINUTO = 10 # Rate Limiting

def sanitizar_entrada(texto):
    """ Mitigação contra Data Poisoning (Remove caracteres destrutivos) """
    if not isinstance(texto, str): return texto
    return re.sub(r'[<>\$;\']', '', texto)

def verificar_rate_limit(ip_cliente):
    """ Mitigação contra Ataques de DDoS na nuvem """
    tempo_atual = time.time()
    if ip_cliente not in controle_ips:
        controle_ips[ip_cliente] = []
    controle_ips[ip_cliente] = [t for t in controle_ips[ip_cliente] if tempo_atual - t < 60]
    
    if len(controle_ips[ip_cliente]) >= MAX_REQUISICOES_POR_MINUTO:
        return False
    controle_ips[ip_cliente].append(tempo_atual)
    return True

# =====================================================================
# ROTAS DO TARPIT (HIGH-INTERACTION) - A ARMADILHA PARA O HACKER
# =====================================================================

@app.route('/postgres/v1/authenticate', methods=['POST'])
def armadilha_login_falso():
    """ 
    Rota falsa que simula a entrada de um banco PostgreSQL.
    Ela atrasa a resposta (Tarpit) e aceita a senha após 3 tentativas 
    para o hacker achar que invadiu com sucesso.
    """
    ip_origem = request.remote_addr
    
    # 1. Aplica mitigação de Rate Limit e Buffer Overflow
    if not verificar_rate_limit(ip_origem):
        return jsonify({"error": "Connection reset by peer"}), 429
    if request.content_length and request.content_length > MAX_PAYLOAD_SIZE:
        return jsonify({"error": "Payload too large"}), 413

    # 2. Registra o atacante silenciosamente na CAIXA PRETA
    dados_recebidos = request.get_json(silent=True) or {}
    log_auditoria = {
        "timestamp": time.ctime(),
        "ip_atacante": ip_origem,
        "acao": "Tentativa de Força Bruta",
        "payload_enviado": {k: sanitizar_entrada(str(v)) for k, v in dados_recebidos.items()}
    }
    banco_dados_seguro.append(log_auditoria)
    print(f"\n[ALERTA SILENCIOSO] Hacker {ip_origem} detectado e logado!")

    # 3. O EFEITO TARPIT (Poço de Piche) - Prende a conexão do hacker por 3 segundos
    time.sleep(3) 

    # 4. A ISCA DE ALTA INTERAÇÃO: Deixa o hacker entrar na 3ª tentativa
    tentativas_login[ip_origem] = tentativas_login.get(ip_origem, 0) + 1
    
    if tentativas_login[ip_origem] >= 3 or dados_recebidos.get("password") == "admin123":
        # Entrega o prêmio falso para mantê-lo ocupado
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
        # Finge que a senha está errada para ele tentar de novo
        return jsonify({"error": "Authentication failed for user"}), 401

if __name__ == '__main__':
    print("=== HONEYDB TARPIT INICIADO - AGUARDANDO INVASORES ===")
    app.run(host='0.0.0.0', port=5000)
