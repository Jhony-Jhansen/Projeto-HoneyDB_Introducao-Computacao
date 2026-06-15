from flask import Flask, request, jsonify
import re
import time

app = Flask(__name__)

# --- SIMULAÇÃO DE BANCO DE DADOS E MEMÓRIA ---
banco_dados_seguro = []
controle_ips = {} # Memória para o Rate Limiting

# --- CONFIGURAÇÕES DE SEGURANÇA ---
MAX_PAYLOAD_SIZE = 1024 # Evita Buffer Overflow (Max 1KB)
MAX_REQUISICOES_POR_MINUTO = 5 # Rate Limiting contra Força Bruta/DDoS

def sanitizar_entrada(texto):
    """
    Mitigação contra Data Poisoning / Injection.
    Remove caracteres perigosos como < > $ ; e aspas simples.
    """
    if not isinstance(texto, str): return texto
    texto_limpo = re.sub(r'[<>\$;\']', '', texto)
    return texto_limpo

def verificar_rate_limit(ip_cliente):
    """
    Mitigação contra Ataques de Força Bruta e DDoS.
    """
    tempo_atual = time.time()
    
    # Se o IP nunca acessou, cria o registro
    if ip_cliente not in controle_ips:
        controle_ips[ip_cliente] = []
        
    # Limpa requisições antigas (mais de 60 segundos atrás)
    controle_ips[ip_cliente] = [t for t in controle_ips[ip_cliente] if tempo_atual - t < 60]
    
    # Verifica se passou do limite
    if len(controle_ips[ip_cliente]) >= MAX_REQUISICOES_POR_MINUTO:
        return False # Bloqueia
        
    # Registra nova requisição
    controle_ips[ip_cliente].append(tempo_atual)
    return True # Permite

@app.route('/api/receber_logs', methods=['POST'])
def receber_logs_isca():
    ip_origem = request.remote_addr
    
    # 1. MITIGAÇÃO: Rate Limiting (Flood / Força Bruta)
    if not verificar_rate_limit(ip_origem):
        return jsonify({"erro": "RATE_LIMIT_EXCEDIDO", "mensagem": "Múltiplas requisições. IP bloqueado temporariamente."}), 429

    # 2. MITIGAÇÃO: Buffer Overflow (Estouro de Memória)
    if request.content_length and request.content_length > MAX_PAYLOAD_SIZE:
        return jsonify({"erro": "PAYLOAD_TOO_LARGE", "mensagem": "O pacote excede o tamanho máximo permitido de segurança."}), 413

    # Tenta ler o JSON enviado
    try:
        dados_recebidos = request.get_json()
    except Exception:
        return jsonify({"erro": "BAD_REQUEST", "mensagem": "Formato de dados inválido. Exige JSON."}), 400

    # 3. MITIGAÇÃO: Data Sanitization (Prevenção de Injection)
    dados_higienizados = {}
    for chave, valor in dados_recebidos.items():
        chave_segura = sanitizar_entrada(str(chave))
        valor_seguro = sanitizar_entrada(str(valor))
        dados_higienizados[chave_segura] = valor_seguro
        
    # Auditoria e Salvamento Seguro
    dados_higienizados["timestamp_banco"] = time.ctime()
    dados_higienizados["ip_rastreado"] = ip_origem
    dados_higienizados["status_seguranca"] = "DADOS_HIGIENIZADOS"
    
    banco_dados_seguro.append(dados_higienizados)
    
    print("\n[!] NOVO ALERTA GRAVADO NO BANCO DE DADOS:")
    print(dados_higienizados)

    return jsonify({"status": "sucesso", "mensagem": "Log criptografado e salvo na caixa preta."}), 201

if __name__ == '__main__':
    # Roda a API segura na porta 5000
    print("=== API DO HONEYDB INICIADA - SISTEMA DE DEFESA ATIVO ===")
    app.run(host='0.0.0.0', port=5000)
