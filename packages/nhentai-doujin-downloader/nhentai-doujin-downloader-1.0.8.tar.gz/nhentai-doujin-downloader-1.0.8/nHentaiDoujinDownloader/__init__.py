import requests
def downloadDoujin(idNum, pageCount):
    """
    import importlib  
    nh = importlib.import_module("nHentaiDoujinDownloader")
    print(nh)
    """
    x = 1
    pStrCount = str(pageCount)
    str_ID_Name = str(idNum)
    pCount = int(pageCount) + 1
    while x != pCount:
        fileName = "{}t.jpg".format(x)
        strIdNum = str(idNum)
        f = open(fileName,'wb')
        websites = "https://t.nhentai.net/galleries/{}/{}".format(strIdNum, fileName)
        f.write(requests.get(websites).content)
        f.close()
        x+=1
    EXIT_MESSAGE = "-------------------------------\nExit Status Code 200.\n{} Pages of {} Downloaded Successfully.\n-------------------------------".format(pStrCount, str_ID_Name)
    print(EXIT_MESSAGE)