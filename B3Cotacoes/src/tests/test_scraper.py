import pytest
from pathlib import Path
from b3_cotacoes.scraper import B3Scraper

@pytest.fixture
def scraper():
    scraper = B3Scraper(headless=True)
    yield scraper
    scraper.close()

def test_scraper_inicializacao(scraper):
    assert scraper is not None