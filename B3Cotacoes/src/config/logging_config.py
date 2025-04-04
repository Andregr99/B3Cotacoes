import logging
import os
from pathlib import Path

def configurar_logging(debug: bool = False):
    try:
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_dir / "automacao.log"),
                logging.StreamHandler()
            ]
        )
    except Exception as e:
        logging.error(f"Falha ao configurar logging: {str(e)}")
        raise