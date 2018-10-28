def getFileName(url):
    pos = url.rfind("/")
    filename = url[pos+1:]
    return filename