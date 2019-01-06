from src import Scrapper
from src import dataCleaningUtils

Scrapper.scraping(Scrapper.urlBase)

dataCleaningUtils.compactFile();