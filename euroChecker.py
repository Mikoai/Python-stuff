import requests
import re
import json

listOfWebsites = ['https://www.nbp.pl/kursy/KursyA.html', 'https://kursy-walut.mybank.pl/', 'https://api.nbp.pl/api/exchangerates/rates/c/eur/', 'https://internetowykantor.pl/cms/currency_money/?last-update=1589121736&nocache=1589121758039',
                  'https://kursy-na-zywo.mybank.pl/automat/kursy.json']

dictOfAllAskPrices = {}


class Observer:
    def __init__(self, link, mean, dict):
        self.link = link
        self.meanEUR = mean
        self.dictOfAllPrices = dict

    def keyFromValue(self, val):
        for k, v in self.dictOfAllPrices.items():
            if val == v:
                return k

    def askFromWebsite(self, setOfPrices):
        ask = 256
        for x in setOfPrices:
            if x > self.meanEUR and x < ask:
                ask = x

        self.dictOfAllPrices[self.link] = ask

    def updateBestAsk(self, setOfPrices):
        self.askFromWebsite(setOfPrices)
        bestAsk = 256
        for x in self.dictOfAllPrices.values():
            if x < bestAsk:
                bestAsk = x
        print("Updating...\n Current best ask: {} from {}".format(
            bestAsk, self.keyFromValue(bestAsk)))

    def buyBestAsk(self, setOfPrices):
        self.askFromWebsite(setOfPrices)
        bestAsk = 256
        for x in self.dictOfAllPrices.values():
            if x < bestAsk:
                bestAsk = x
        print("Buying EUR with unit price of {} from {}".format(
            bestAsk, self.keyFromValue(bestAsk)))


class MultiFuns():

    def __init__(self, link, mean):
        self.link = link
        self.meanEUR = mean

    def funA(self):
        r = requests.get(self.link)
        listaHTML = r.text.splitlines()
        eurList = re.findall('(.*(\s?EUR\s?).*)', r.text)
        eurPrices = re.findall('(\d[\.|,]\d\d\d\d)', str(eurList))
        return eurPrices

    def funB(self):
        r = requests.get(self.link)
        prices = json.loads(r.text.lower())
        if 'eurpln' in prices:
            return prices['eurpln']
        elif 'rates' in prices:
            if 'eurpln' in prices['rates']:
                return prices['rates']['eurpln']
            elif 'eur' in prices['rates']:
                return prices['rates']['eur']

    def funC(self):
        r = requests.get(self.link)
        regex = r"((\s?EUR\s?).*)"
        listaHTML = r.text.splitlines()
        founds = []
        for i in listaHTML:
            if(re.search(regex, i)):
                for j in range(listaHTML.index(i), listaHTML.index(i) + 2):
                    if(re.search('(\d[\.|,]\d\d\d\d)', listaHTML[j])):
                        founds.append(listaHTML[j])

        eurs = re.findall('(\d[\.|,]\d\d\d\d)', str(founds))
        return eurs

    def funD(self):
        r = requests.get(self.link)
        eurPrices = re.findall('(\d[\.|,]\d\d\d\d)', r.text)
        return eurPrices

    def tryFunACD(self):
        listOfEUR = []
        try:
            listOfPrices = MultiFuns(self.link, self.meanEUR).funA()
            for x in listOfPrices:
                if isinstance(x, str):
                    if float(x.replace(",", ".")) > (meanEUR - 0.1) and float(x.replace(",", ".")) < (meanEUR + 0.1):
                        listOfEUR.append(float(x.replace(",", ".")))
                elif x > (meanEUR - 0.1) and x < (meanEUR + 0.1):
                    listOfEUR.append(x)

            listOfPrices = MultiFuns(self.link, self.meanEUR).funC()
            for x in listOfPrices:
                if isinstance(x, str):
                    if float(x.replace(",", ".")) > (meanEUR - 0.1) and float(x.replace(",", ".")) < (meanEUR + 0.1):
                        listOfEUR.append(float(x.replace(",", ".")))
                elif x > (meanEUR - 0.1) and x < (meanEUR + 0.1):
                    listOfEUR.append(x)

            listOfPrices = MultiFuns(self.link, self.meanEUR).funD()
            for x in listOfPrices:
                if isinstance(x, str):
                    if float(x.replace(",", ".")) > (meanEUR - 0.1) and float(x.replace(",", ".")) < (meanEUR + 0.1):
                        listOfEUR.append(float(x.replace(",", ".")))
                elif x > (meanEUR - 0.1) and x < (meanEUR + 0.1):
                    listOfEUR.append(x)
        except:
            pass

        return listOfEUR

    def tryFunB(self):
        listOfJsonPrices = []
        try:
            jsonDict = MultiFuns(self.link, self.meanEUR).funB()
        except:
            pass

        try:
            for x in jsonDict.values():

                if float(x.replace(",", ".")) > (meanEUR - 0.1) and float(x.replace(",", ".")) < (meanEUR + 0.1):
                    listOfJsonPrices.append(float(x.replace(",", ".")))

        except:
            pass

        return listOfJsonPrices

    def oneForAll(self):
        if not self.tryFunB():
            return set(self.tryFunACD())
        else:
            return set(self.tryFunB())


meanEUR = float(MultiFuns('https://www.nbp.pl/kursy/KursyA.html',
                          None).funC()[0].replace(",", "."))


for website in listOfWebsites:
    Observer(website, meanEUR, dictOfAllAskPrices).updateBestAsk(
        MultiFuns(website, meanEUR).oneForAll())

Observer(listOfWebsites[0], meanEUR, dictOfAllAskPrices).buyBestAsk(
    MultiFuns(listOfWebsites[0], meanEUR).oneForAll())
