import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent
B3_URL = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/cotacoes/outros-ativos.htm"
TIMEOUT = int(os.getenv("TIMEOUT", 5000))
ARQUIVO_DADOS = BASE_DIR / "data" / "B3Acoes.xlsx"

ARQUIVO_DADOS.parent.mkdir(parents=True, exist_ok=True)