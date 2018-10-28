import urllib3
import csv
import datetime
import shutil
import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


delimiter = ";"
altDelimiter = ","
lineterminator = '\r'


def getFieldNames() -> object:
    fieldnames = ['imgName', 'code', 'description', 'price', 'image', 'puntuation', 'altImage', 'stock', 'date']
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


def eof(html):
    fin = html.find('h1', class_="a-size-medium a-spacing-none a-spacing-top-mini a-color-base a-text-normal")
    if (fin == None):
        return 0
    return 1

def createFile(fileName):
    with open(fileName, 'w') as csvfile:
        fieldnames = getFieldNames()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter, quotechar=delimiter, quoting=csv.QUOTE_MINIMAL, lineterminator=lineterminator)
        writer.writeheader()


def createRow(imgName, fileName, code, price, description, image, puntuation, imgAlt, stock):
    with open(fileName, 'a') as csvfile:
        fieldnames = getFieldNames()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\r')
        if imgName != None:
            imgName = imgName.replace(delimiter, altDelimiter)
        if code != None:
            code = code.replace(delimiter, altDelimiter)
        if description != None:
            description = description.replace(delimiter, altDelimiter)
        if price != None:
            price = price.replace(delimiter, altDelimiter)
        if image != None:
            image = image.replace(delimiter, altDelimiter)
        if puntuation != None:
            puntuation = puntuation.replace(delimiter, altDelimiter)
        if imgAlt != None:
            imgAlt = imgAlt.replace(delimiter, altDelimiter)
        if stock != None:
            stock = stock.replace(delimiter, altDelimiter)
        writer.writerow({
            'imgName': imgName,
            'code': code,
            'description': description,
            'price': price,
            'image': image,
            'puntuation': puntuation,
            'altImage' : imgAlt,
            'stock' : stock,
            'date':datetime.datetime.now().__str__()
        })

def downloadImg(url, folder, file):
    response = requests.get(url, stream=True)
    fileLoc = folder+"/"+file
    with open(fileLoc, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response