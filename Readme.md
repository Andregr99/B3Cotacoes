# 🚀 **Automatização de Cotações da B3 com Playwright**

Este projeto realiza a extração automática de cotações de ativos na B3, capturando informações como preço, oscilação, data e hora. Em seguida, os dados são atualizados em uma planilha utilizando Python, Playwright e Pandas.. **O código está estruturado seguindo boas práticas, incluindo tratamento de erros, logging e execução parametrizada via linha de comando.**

## ⚙️ **Funcionalidades**  

✅ **Busca automática de cotações:** Extrai o preço atual, variação percentual, data e hora diretamente do site da B3.

✅ **Leitura de planilhas:** Obtém os símbolos dos ativos a partir de um arquivo Excel.

✅ **Execução parametrizada:** Pode ser rodado em modo headless ou interativo.

✅ **Logging estruturado:** Registra eventos e possíveis erros para facilitar a depuração.

✅ **Tratamento de exceções:** Evita falhas inesperadas, tornando a automação mais confiável.

## 🚀 **Tecnologias Utilizadas**

- **Python 3.x:** Linguagem principal do projeto.
- **Playwright:** Biblioteca para automação de navegação web.
- **Pandas:** Manipulação e leitura de planilhas Excel.
- **Logging:** Registro estruturado de eventos.
- **Argparse:** Permite parametrização via linha de comando.

## ⚙️ **Instalação e Execução**  

1️⃣ **Clone o repositório:**

git clone https://github.com/Andregr99/B3Cotacoes.git

cd B3Cotacoes

2️⃣ **Crie e ative um ambiente virtual:**

python -m venv venv
Windows:
venv\Scripts\activate
Linux/Mac:
source venv/bin/activate

3️⃣ **Instale as dependências:**

pip install -r requirements.txt

4️⃣ **Execute o script**

Modo interativo (abre o navegador):
python projeto_b3.py B3Acoes.xlsx

Modo headless (sem abrir o navegador):sh
python projeto_b3.py B3Acoes.xlsx --headless
