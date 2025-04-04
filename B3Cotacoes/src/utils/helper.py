from playwright.sync_api import Locator

def extrair_texto(locator: Locator, padrao: str = "______") -> str:
    try:
        return locator.text_content().strip() or padrao
    except Exception:
        return padrao

def formatar_data(data: str) -> str:
    try:
        return "-".join(reversed(data.split("/")))
    except Exception:
        return data