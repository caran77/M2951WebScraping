from bs4 import BeautifulSoup
import urllib3
import csv
import datetime
import time

def getFieldNames() -> object:
    fieldnames = ['code', 'description', 'price', 'image', 'puntuation', 'altImage', 'fecha']
    return fieldnames


def download(url, num_retries=2):
    print('Downloading:', url)
    response = None
    if (num_retries == 0):
        return None
    http = urllib3.PoolManager()
    try:
        response = http.request('GET', url)
    except Exception:
        download(url, num_retries - 1)
    return response.data


def createFile(fileName):
    with open(fileName, 'w') as csvfile:
        fieldnames = getFieldNames()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\r')
        writer.writeheader()


def createRow(fileName, code, price, description, image, puntuation, imgAlt):
    with open(fileName, 'a') as csvfile:
        fieldnames = getFieldNames()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\r')
        writer.writerow({'code' : code, 'description': description, 'price': price, 'image': image, 'puntuation': puntuation, 'altImage' : imgAlt, 'fecha':datetime.datetime.now().__str__()})


def getPrice(html):
    price = None
    spanprice = html.find('span', class_="a-size-base")
    if (spanprice != 'None'):
        try:
            price = spanprice.contents[0]
        except(Exception):
            price = None
    return price


def getPuntuation(html):
    puntuation = None
    spanpunt = html.find_all('span', class_="a-icon-alt")
    if (spanpunt != None):
        try:
            if (spanpunt[0].contents[0] != 'Prime'):
                puntuation = spanpunt[0].contents[0]
            else:
                puntuation = spanpunt[1].contents[0]
        except(Exception):
            puntuation = None
    return puntuation


def getImageURL (html):
    urlImg = None
    img = html.img
    if (img != None):
        try:
            urlImg = img['src']
        except(Exception):
            urlImg = None
    return urlImg


def getImageAlt (html):
    altImg = None
    alt = html.img
    if (alt != None):
        try:
            altImg = alt['alt']
        except(Exception):
            altImg = None
    return altImg


def getDescription(html):
    description = None
    desc =  html.find('a', class_="s-color-twister-title-link")
    if (desc != None):
        try:
            description = desc['title']
        except(Exception):
            description = None
    return description


def getCode(html):
    code = None
    for codeVal in html.find_all('div', class_="a-column a-span5 a-span-last"):
        divCode = codeVal.find('div', class_="a-row a-spacing-mini")
        if divCode != None:
            spanCode = divCode.find('span')
            if (spanCode != None):
                try:
                    code = spanCode['name']
                except(Exception):
                    print("Code error")
    return code


def eof(html):
    fin = html.find('h1', class_="a-size-medium a-spacing-none a-spacing-top-mini a-color-base a-text-normal")
    if (fin == None):
        return 0
    return 1


def scraping(url):
    createFile('miFichero.csv')
    x = 1
    finaliza = 0
    while finaliza == 0:
        http = download(url + "&page=" + x.__str__(), 3)
        time.sleep(1)
        finaliza = 1
        if not (http is None):
            soup = BeautifulSoup(http, 'html.parser')
            finaliza = eof(soup)
            all_a = soup.find_all('div', class_="a-fixed-left-grid-inner")
            # print(all_a)
            for a in all_a:
                code = getCode(a)
                imgURL = getImageURL (a)
                imgAlt = getImageAlt (a)
                price = getPrice(a)
                puntuation = getPuntuation(a)
                description = getDescription(a)
                try:
                    createRow('miFichero.csv', code, price, description, imgURL, puntuation, imgAlt)
                except(Exception):
                    if (code == None):
                        print("Error desconocido")
                    else:
                        print("Error "+code)
        x = x + 1
    print("x "+ x.__str__())

scraping("https://www.amazon.es/s/field-keywords=nikon")
