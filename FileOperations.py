import urllib3
import csv
import datetime
import shutil
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getFieldNames() -> object:
    fieldnames = ['imgName', 'code', 'description', 'price', 'image', 'puntuation', 'altImage', 'fecha']
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
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\r')
        writer.writeheader()


def createRow(imgName, fileName, code, price, description, image, puntuation, imgAlt):
    with open(fileName, 'a') as csvfile:
        fieldnames = getFieldNames()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\r')
        writer.writerow({'imgName': imgName, 'code': code, 'description': description, 'price': price, 'image': image, 'puntuation': puntuation, 'altImage' : imgAlt, 'fecha':datetime.datetime.now().__str__()})

def downloadImg(url, folder, file):
    response = requests.get(url, stream=True)
    fileLoc = folder+"/"+file
    with open(fileLoc, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response