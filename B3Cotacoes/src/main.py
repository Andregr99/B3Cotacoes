import argparse
import logging
from pathlib import Path
from config.logging_config import configurar_logging
from config.settings import ARQUIVO_DADOS, BASE_DIR
from b3_cotacoes import B3Scraper
from utils.file_handler import ExcelHandler

def parse_args():
    parser = argparse.ArgumentParser(
        description="Automação de scraping de cotações da B3",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--arquivo",
        type=Path,
        default=ARQUIVO_DADOS,
        help="Caminho do arquivo Excel com os símbolos"
    )
    parser.add_argument(

        "--headless",
        action="store_true",
        help="Executar o navegador em modo headless"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativar modo debug para logging detalhado"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    configurar_logging(debug=args.debug)
    
    if not args.arquivo.exists():
        logging.error(f"Arquivo não encontrado: {args.arquivo.resolve()}")
        logging.info(f"Por favor, crie a pasta 'data' e coloque o arquivo 'B3Acoes.xlsx' nela")
        return

    scraper = None
    try:
        logging.info(f"Iniciando automação com arquivo: {args.arquivo}")
        scraper = B3Scraper(headless=args.headless)
        resultados = scraper.executar(args.arquivo)
        output_path = BASE_DIR / "outputs" / "resultados.xlsx"
        output_path.parent.mkdir(exist_ok=True)
        ExcelHandler.salvar_resultados(resultados, output_path)
        logging.info(f"Concluído! Resultados salvos em: {output_path}")
    except Exception as e:
        logging.error(f"Erro na automação: {str(e)}", exc_info=args.debug)
        raise
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()