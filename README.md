# HoneyDB: Módulo de Alertas via Webhook

> **Aviso:** Esta *branch* contém uma funcionalidade específica do projeto HoneyDB. Para ver a documentação geral, visite a branch "main".

## Sobre esta Branch

Nesta versão, o HoneyDB integra conceitos de Redes e APIs para fornecer monitoramento em tempo real para as equipes de **SOC (Security Operations Center)**.

### Principais Funcionalidades Implementadas aqui:
* **Integração de Rede Externa:** Uso da biblioteca `requests` para estabelecer comunicação com servidores de terceiros.
* **Alertas em Tempo Real:** Disparo de mensagens automáticas via Webhook.
* **Prova de Conceito (PoC) com Discord:** O sistema formata os logs de invasão (IP e Ação) em arquivos JSON e os envia via requisição POST para um canal de segurança no Discord, alertando a equipe de TI no exato momento da tentativa de invasão.
