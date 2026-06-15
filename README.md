# HoneyDB - Deception Technology 

Repositório destinado ao projeto final da disciplina de **Introdução à Computação**

# Sobre o Projeto
Este projeto explora a intersecção entre **Cybersegurança** e **Banco de Dados**, implementando o conceito de *Deception Technology*. foi criado um dispositivo IoT de borda (isca) que simula um banco de dados vulnerável para atrair atacantes (Ransomware/Hackers). 

Enquanto o atacante acredita estar invadindo um sistema real, o dispositivo coleta suas informações e envia para esta API central, que atua como uma "Caixa Preta" de auditoria.

# Camadas de Defesa (Implementadas nesta API)
Este código (`app.py`) foi desenvolvido em Python utilizando o framework **Flask** e conta com 3 mecanismos rigorosos de mitigação de falhas de Software e Rede:

1. **Mitigação contra DDoS e Força Bruta:** Algoritmo de *Rate Limiting* (Máx. 5 requisições/minuto por IP).
2. **Mitigação contra Buffer Overflow (Estouro de Memória):** Limite estrito de `MAX_PAYLOAD_SIZE = 1024 bytes`. Pacotes maiores são sumariamente dropados.
3. **Mitigação contra Data Poisoning (Injeção SQL/NoSQL):** Função de higienização de entrada (*Data Sanitization*) baseada em Regex, que limpa caracteres perigosos antes da gravação no banco de dados isolado.

# Hardware associado
A contraparte física deste projeto (O Dispositivo de Borda) possui mitigação contra Violação de Gabinete (Tamper) e Sobreaquecimento (DDoS físico), desenvolvido em C++ e simulado via Tinkercad.

**Autor:** João Pedro Valadares Maciel de Oliveira
**Foco Profissional:** Cybersegurança e Banco de Dados
