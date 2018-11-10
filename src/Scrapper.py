import time

from bs4 import BeautifulSoup

from src import utils, FileOperations, HTMLGetters

urlBase = "https://www.amazon.es/s/field-keywords="
fileName = 'data/productData.csv'
sleepTime = 1
retries = 3
parser = 'html.parser'
search = ["nikon", "canon", "leica", "fujifilm"]

def scraping(url):
    FileOperations.createFile(fileName)
    for searchConcept in search:
        x = 1
        finaliza = 0
        while finaliza == 0:
            http = FileOperations.download(url + searchConcept + "&page=" + x.__str__(), retries)
            time.sleep(sleepTime)
            finaliza = 1
            if not (http is None):
                soup = BeautifulSoup(http, parser)
                finaliza = FileOperations.eof(soup)
                all_a = soup.find_all('div', class_="a-fixed-left-grid-inner")
                treatDiv(all_a)
            x = x + 1
        print("x "+ x.__str__())


def treatDiv(all_a):
    for a in all_a:
        code = HTMLGetters.getCode(a)
        imgURL = HTMLGetters.getImageURL(a)
        imgAlt = HTMLGetters.getImageAlt(a)
        price = HTMLGetters.getPrice(a)
        puntuation = HTMLGetters.getPuntuation(a)
        description = HTMLGetters.getDescription(a)
        stock = HTMLGetters.getStock(a)
        imgName = None
        if (imgURL != None):
            imgName = utils.getFileName(imgURL)
            FileOperations.downloadImg(imgURL, 'img', imgName)
        try:
            FileOperations.createRow(imgName, fileName, code, price, description, imgURL, puntuation, imgAlt, stock)
        except(Exception):
            if (code == None):
                print("Error desconocido")
            else:
                print("Error " + code)
