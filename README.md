# HoneyDB: Módulo Firewall Dinâmico & GeoIP

> **Aviso:** Esta *branch* contém uma funcionalidade específica do projeto HoneyDB. Para ver a documentação geral, visite a branch "main".

## 🛠️ Sobre esta Branch

Nesta versão, o HoneyDB foca no isolamento de perímetro e na rastreabilidade, atuando não apenas como uma isca, mas como um mecanismo de **Defesa Ativa**.

### Principais Funcionalidades Implementadas aqui:
* **Rastreamento Geográfico (GeoIP):** Integração via API REST (`requests`) para rastrear o país e a cidade de origem do IP do atacante em tempo real.
* **Firewall Dinâmico:** Implementação de uma *Blacklist* na memória do sistema.
* **Banimento Automático:** Assim que o atacante cai na isca e tem suas intenções confirmadas, seu IP é banido permanentemente, retornando o status HTTP 403 (Forbidden) para qualquer tentativa futura.
