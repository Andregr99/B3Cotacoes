import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import argparse

def configurar_logging():
    """Configura o sistema de logging."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ler_dados(nome_do_arquivo: str) -> pd.DataFrame:
    """Lê os dados da planilha e retorna um DataFrame."""
    try:
        df = pd.read_excel(nome_do_arquivo, dtype=str)
        df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas
        logging.info(f"Arquivo '{nome_do_arquivo}' carregado com sucesso.")
        return df
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {nome_do_arquivo}: {e}")
        raise

def fechar_banner_cookies(page):
    """Verifica se o botão de fechar cookies está presente e clica nele."""
    try:
        btn_cookies = page.locator('xpath=//*[@id="onetrust-close-btn-container"]/button')
        if btn_cookies.is_visible():
            btn_cookies.click()
            logging.info("Banner de cookies fechado.")
            page.wait_for_timeout(2000)
    except Exception as e:
        logging.warning(f"Erro ao fechar o banner de cookies: {e}")

def buscar_dados_b3(symbol, page):
    """Busca os dados da ação no site da B3 e retorna os valores extraídos."""
    try:
        input_busca = page.locator('#txtCampoPesquisa')
        input_busca.fill(symbol)
        page.wait_for_timeout(1000)
        input_busca.press("Enter")

        # Espera explícita para garantir que os elementos carreguem
        page.wait_for_selector('xpath=//*[@id="cotacaoAtivo"]', timeout=5000)
        page.wait_for_timeout(1000)

        preco_element = page.locator('xpath=//*[@id="cotacaoAtivo"]')
        oscilacao_element = page.locator('xpath=//*[@id="oscilacaoAtivo"]')
        data_element = page.locator('xpath=//*[@id="dataConsulta"]')
        hora_element = page.locator('xpath=//*[@id="horaConsulta"]')

        preco = preco_element.inner_text().strip() if preco_element.count() else None
        oscilacao = oscilacao_element.inner_text().strip() if oscilacao_element.count() else None
        data = data_element.inner_text().strip() if data_element.count() else None
        hora = hora_element.inner_text().strip() if hora_element.count() else None

        logging.info(f"Dados coletados para {symbol}: Preço {preco}, Oscilação {oscilacao}, Data {data}, Hora {hora}")
        return preco, oscilacao, data, hora

    except PlaywrightTimeoutError:
        logging.error(f"Timeout ao buscar dados para {symbol}")
        return None, None, None, None
    except Exception as e:
        logging.error(f"Erro inesperado ao buscar dados para {symbol}: {e}")
        return None, None, None, None

def executar_automacao(nome_do_arquivo: str, headless: bool):
    """Executa o processo de automação para buscar cotações da B3."""
    df = ler_dados(nome_do_arquivo)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        try:
            logging.info("Acessando a página da B3...")
            page.goto("https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/cotacoes/outros-ativos.htm")
            
            fechar_banner_cookies(page)
            page.wait_for_timeout(5000)

            for i, row in df.iterrows():
                simbolo = str(row["Símbolo"]).strip()
                logging.info(f"Buscando dados para: {simbolo}")

                preco, oscilacao, data, hora = buscar_dados_b3(simbolo, page)

                if preco:
                    df.at[i, "Preço"] = str(preco)
                    df.at[i, "Oscilação"] = str(oscilacao)
                    df.at[i, "Data"] = str(data) if data else ""
                    df.at[i, "Hora"] = str(hora) if hora else ""

                page.wait_for_timeout(3000)

            df.to_excel(nome_do_arquivo, index=False)
            logging.info(f"Dados salvos em '{nome_do_arquivo}'.")

        except PlaywrightTimeoutError:
            logging.error("Erro ao carregar a página da B3.")
        finally:
            browser.close()

def main():
    configurar_logging()

    parser = argparse.ArgumentParser(description="Automação para buscar cotações na B3 com Playwright.")
    parser.add_argument("arquivo", type=str, nargs="?", default="B3Ações.xlsx",
                        help="Caminho do arquivo Excel com os símbolos das ações (padrão: B3Ações.xlsx).")
    parser.add_argument("--headless", action="store_true", help="Executar o navegador em modo headless.")
    args = parser.parse_args()

    executar_automacao(args.arquivo, args.headless)

if __name__ == "__main__":
    main()
