from bs4 import BeautifulSoup


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