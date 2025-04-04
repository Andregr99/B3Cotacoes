# 🚀 **Automatização de Cotações da B3**

Este projeto realiza a extração automática de cotações de ativos na B3, capturando informações como preço, oscilação, data e hora. Os dados são processados e armazenados de forma estruturada, seguindo boas práticas de desenvolvimento, incluindo tratamento de erros, logging e organização modular do código.


## ⚙️ **Funcionalidades**  

✅ **Extração de dados:** Captura informações de cotações diretamente da B3.

✅ **Armazenamento de dados:** Salva os resultados em arquivos Excel para fácil acesso e análise.

✅ **Logging estruturado:** Registra eventos e erros durante a execução para facilitar a depuração.

✅ **Organização modular:** Código dividido em módulos específicos para melhor manutenibilidade.

✅ **Tratamento de exceções:** Implementa mecanismos robustos para lidar com erros inesperados.


## 🚀 **Tecnologias Utilizadas**

**Python 3.10+** (principal)

**Playwright** (automação web e scraping)

**Pandas** (manipulação de dados em Excel)

**Logging** (rastreamento de execução)

**Argparse** (parâmetros via CLI)


## ⚙️ **Instalação e Execução** 

**Pré-requisitos**

Python 3.10 ou superior
Git (para clonar o repositório)

1️⃣ Clone o repositório:

git clone https://github.com/Andregr99/B3Cotacoes.git
cd B3Cotacoes

2️⃣ Crie e ative um ambiente virtual:

python -m venv venv
Windows:
venv\Scripts\activate
Linux/Mac:
source venv/bin/activate

3️⃣ Instale as dependências e o Playwright:

pip install -e .
playwright install
playwright install-deps

🧪 Testes
Para executar os testes unitários:

python -m pytest tests/

ℹ️ Suporte ao Playwright

Caso encontre problemas com a instalação do Playwright:

No Windows, execute como Administrador

No Linux, pode ser necessário instalar dependências adicionais:
sudo apt-get install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

