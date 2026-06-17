# HoneyDB: Módulo Tarpit & High-Interaction

> **Aviso:** Esta *branch* contém uma funcionalidade específica do projeto HoneyDB. Para ver a documentação geral, visite a branch "main".

## Sobre esta Branch

Nesta versão, o HoneyDB evolui de um *Low-Interaction Honeypot* para um **High-Interaction Honeypot**. Implementamos o conceito de **Tarpitting (Poço de Piche)**, uma técnica de defesa ativa na rede.

### Principais Funcionalidades Implementadas aqui:
* **Simulação de PostgreSQL:** O sistema responde com cabeçalhos e estruturas de dados falsas (ex: `tb_senhas_diretoria`) simulando um banco de dados relacional complexo.
* **Tarpitting Activo:** Em vez de apenas bloquear o atacante, o sistema "prende" a conexão dele usando `time.sleep()`, consumindo os recursos do hacker e atrasando ataques automatizados.
* **Falso Sucesso (Deception):** Após 3 tentativas, o sistema finge que o atacante teve sucesso no *login*, entregando a ele a base de dados falsa isolada, enquanto ele é monitorado silenciosamente.
