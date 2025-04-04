import logging
import pandas as pd
from playwright.sync_api import sync_playwright
from pathlib import Path
from typing import List, Dict, Optional
from config.settings import B3_URL, TIMEOUT
from utils.helper import extrair_texto, formatar_data
from .exceptions import DadosNaoCarregadosError

class B3Scraper:
    def __init__(self, headless: bool = True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=[
                "--start-maximized",
                "--window-position=0,0",  
                "--disable-infobars"
            ],
            channel="chrome",
            slow_mo=100 
        )
        
        # Contexto com viewport máximo
        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            no_viewport=False  
        )
        
        self.page = self.context.new_page()
        
        if not headless:
            self.page.evaluate("window.moveTo(0,0);window.resizeTo(screen.width,screen.height);")
            self.page.keyboard.press("F11")
        
        logging.info("Navegador pronto em tela cheia")

    def _fechar_banner_cookies(self):
        try:
            selectors = [
                '#onetrust-close-btn-container',
                'button[aria-label="Fechar"]',
                '.btn-close'
            ]
            
            for selector in selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    self.page.wait_for_timeout(500)  
                    break
                    
        except Exception as e:
            logging.warning(f"Erro ao fechar banners: {str(e)}")

    def _buscar_dados_acao(self, symbol: str) -> Dict[str, str]:
        try:
            self.page.fill('#txtCampoPesquisa', symbol, timeout=5000)
            self.page.press('#txtCampoPesquisa', 'Enter', timeout=5000)
            
            self.page.wait_for_function(
                """() => {
                    const el = document.querySelector('#cotacaoAtivo');
                    return el && el.innerText !== '______';
                }""",
                timeout=TIMEOUT
            )
            
            return {
                'symbol': symbol,
                'preco': extrair_texto(self.page.locator('#cotacaoAtivo')),
                'oscilacao': extrair_texto(self.page.locator('#oscilacaoAtivo')),
                'data': formatar_data(extrair_texto(self.page.locator('#dataConsulta'))),
                'hora': extrair_texto(self.page.locator('#horaConsulta'))
            }
            
        except Exception as e:
            logging.error(f"Falha ao buscar {symbol}: {str(e)}")
            raise DadosNaoCarregadosError(symbol)

    def executar(self, arquivo_dados: Path) -> pd.DataFrame:
        try:            
            self.page.goto(
                url=B3_URL,
                timeout=TIMEOUT,
                wait_until="networkidle"  
            )
            self._fechar_banner_cookies()
            
            df = pd.read_excel(arquivo_dados)
            simbolos = df['Símbolo'].unique().tolist()
            
            return pd.DataFrame([
                self._buscar_dados_acao(symbol)
                for symbol in simbolos
                if self._try_get_data(symbol)  
            ])
            
        except Exception as e:
            logging.error(f"Erro fatal: {str(e)}", exc_info=True)
            raise
        finally:
            self.close()

    def _try_get_data(self, symbol: str, max_tries: int = 2) -> bool:
        for attempt in range(max_tries):
            try:
                return self._buscar_dados_acao(symbol)
            except DadosNaoCarregadosError:
                if attempt == max_tries - 1:
                    logging.warning(f"Falha após {max_tries} tentativas para {symbol}")
                    return None
                self.page.wait_for_timeout(2000 * (attempt + 1))  

    def close(self):
        try:
            self._safe_close()
        except Exception as e:
            if "Event loop is closed" in str(e):
                logging.debug("Playwright já encerrado")
            else:
                logging.error(f"Erro inesperado ao fechar: {str(e)}")

    def _safe_close(self):
        resources = [
            ('page', lambda: self.page.close() if hasattr(self, 'page') and not self.page.is_closed() else None),
            ('browser', lambda: self.browser.close() if hasattr(self, 'browser') and not self.browser.is_closed() else None),
            ('playwright', lambda: self.playwright.stop() if hasattr(self, 'playwright') else None)
        ]
        
        for name, closer in reversed(resources):
            try:
                closer()
            except Exception as e:
                logging.debug(f"Erro ao fechar {name}: {str(e)}")