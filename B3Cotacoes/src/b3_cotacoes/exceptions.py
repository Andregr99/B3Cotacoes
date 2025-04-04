class ScraperError(Exception):
    pass

class DadosNaoCarregadosError(ScraperError):
    def __init__(self, symbol: str):
        super().__init__(f"Dados não carregados para o símbolo {symbol} após tentativas")
        self.symbol = symbol