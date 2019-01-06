def getPrice(value):
    posGui = value.find("-")
    if (posGui == -1):
        pos = value.find(" ")
        price = value[pos+1:]
        currency = value[:pos]
        price = price.replace(".", "")
        return price.replace(",", "."), currency, price.replace(",", ".")
    else:
        pos = value.find(" ")
        currency = value[:pos]
        price = value[pos+1:posGui-1]
        posEnd = value.rfind(" ")
        priceEnd = value[posEnd+1:]
        return price.replace(",", "."), currency, priceEnd.replace(",",".")

def getPuntuation(value):
    pos = value.find(" ")
    puntuation = value[:pos]
    puntuation = puntuation.replace(",", ".")
    return puntuation

def getDate(value):
    pos = value.rfind(" ")
    posHour = value.rfind(".")
    day = value[:pos]
    hour = value[pos+1:posHour]
    return day, hour

def getStock(value):
    subString = value[9:]
    pos = subString.find(" ")
    stock = subString[:pos]
    return stock

def deleteInvalidChar(value):
    valueIn = value.replace('\"', "")
    valueIn = valueIn.replace("\'", "")
    valueIn = valueIn.replace('#', "")
    return valueIn

def isValidRow(value):
    if (value in ('Escuchar con Unlimited', 'GRATIS')):
        return 1
    return 0