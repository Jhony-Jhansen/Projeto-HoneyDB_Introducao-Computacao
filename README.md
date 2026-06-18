# HoneyDB: Sistema de Defesa IoT & Deception Technology

Este projeto explora a intersecção entre Cybersegurança, Internet das Coisas (IoT) e Banco de Dados, implementando o conceito avançado de *Deception Technology*. 

O HoneyDB não é apenas um banco de dados, mas sim um **Honeypot** projetado para atuar como uma armadilha contra ataques cibernéticos e violações físicas de hardware.

##  Mitigações Implementadas (Software e Hardware)

O sistema foi desenhado para combater 6 riscos de segurança, utilizando uma API em Python e um microcontrolador (simulado no Tinkercad):

1. **Ataques de Força Bruta / DDoS:** Mitigado via Rate Limiting.
2. **Buffer Overflow:** Mitigado via limitação rigorosa de *Payload Size* (Max 1KB).
3. **Data Poisoning / Injection:** Mitigado via Sanitização de Entrada de Dados (Remoção de caracteres destrutivos).
4. **Sobreaqueecimento de Servidor (Hardware):** Mitigado com sensor de temperatura TMP36 (IoT), que desativa serviços e emite alerta ao ultrapassar 60ºC.
5. **Violação Física do Gabinete (Tamper):** Mitigado via botão de hardware que, se acionado, corta o banco de dados e aciona alertas de violação.
6. **Mimetismo e Tarpitting:** O sistema age como um *High-Interaction Honeypot*, simulando a latência e o ambiente de um banco PostgreSQL complexo para reter o atacante na rede falsa.

##  Arquitetura de Versionamento (Branches)

Este repositório foi organizado utilizando **branches**:

* `main`: Versão estável e inicial do HoneyDB (Low-Interaction) com as defesas de rede básicas.
* `feature/hi-honeypot-tarpit`: Evolução para um *High-Interaction Honeypot* (Poço de Piche), simulando um banco complexo que prende o atacante com falsos sucessos.
* `feature/geoip-firewall`: Implementação avançada de um **Firewall Dinâmico** com rastreamento geográfico em tempo real (API pública) e banimento automático (Blacklist) de IPs maliciosos.

## Link para o Hardware simulado em TINKERCAD:
## https://www.tinkercad.com/things/a8y5SpKMb2c-honeydb?sharecode=b16tYuKeSzUG3_HgfxWUbcf7IHi6jL2dVULFhVtqk9Y
