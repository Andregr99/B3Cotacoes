import pandas as pd
from pathlib import Path
from config.settings import TIMEOUT

class ExcelHandler:
    @staticmethod
    def salvar_resultados(dados: pd.DataFrame, caminho: Path):
        try:
            caminho.parent.mkdir(parents=True, exist_ok=True)
            dados.to_excel(caminho, index=False, engine='openpyxl')
        except Exception as e:
            raise ValueError(f"Falha ao salvar Excel em {caminho}: {str(e)}")