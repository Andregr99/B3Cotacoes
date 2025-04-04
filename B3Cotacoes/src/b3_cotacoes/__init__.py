from .scraper import B3Scraper
__all__ = ['B3Scraper']
def __init__(self, headless: bool = True):
    self._closed = False