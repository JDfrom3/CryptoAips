import urllib2
import json
import time
import datetime
import pandas as pd
import requests
#import matplotlib.pyplot as plt

#TODO
# - Add social analytics from CryptoCompareAPI
# - Add volume spike indicator 
# - can switch name in text in PriceNotification to dynamic from Getjson
# - can change link and pull top 10 coins 


## COINMARKETCAP

# Basic information about coin at present time.
def Getjson(coin):      
	url = "https://api.coinmarketcap.com/v1/ticker/"+coin+"/"
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	return parsed[0]

# Extracts current price and 1h % change from Getjson
def checkPrice(ticker):
	json = Getjson(ticker)
	price = json['price_usd']
	change = json['percent_change_1h']
	return float(price), float(change)

# Takes desired coin and threshold and returns text cointining information about 
# change in price last hour and price if threshold met
def PriceNotification(coins,threshold):

	triggered = 0				#Indicator if threshold tiggered
	email = ''					#Placeholder for email dictionary
	pause = 1					#Pause 1 second before querying coinMK

	for name in coins:
		price, change = checkPrice(name)

		if abs(change) > threshold:
			triggered = 1
			text = {name: name + ' price changed ' + str(change) + ' percent to ' + str(price)}
			print('Threshold triggered '+ str(datetime.datetime.now()))
			email = email + text[name] + "\n"
		time.sleep(pause)
	return email, triggered


## CRYPTOCOMPARE

#Gets list of coins offered on cryptocompare and relevant info (spply,algo,etc.)
def getCoinList(ticker = None):
    req = requests.get('https://min-api.cryptocompare.com/data/all/coinlist').json()
    if ticker == None:
        info = req['Data']
    else:
        info = req['Data'][ticker]
    return info 

# Returns ID cryptocompare assigned to coin for acces from links
def getID(ticker):
    ID = getCoinList(ticker)['Id']
    return ID

#Ex. From BTC to USD, 2000 data points every 3 minutes
def getHistoricalMin(From,To,points,delta):
    req = requests.get('https://min-api.cryptocompare.com/data/histominute?fsym='+From+'&tsym='+To+'&limit='+points+'&aggregate='+delta+'&e=CCCAGG').json()
    info = req['Data']
    priceDat = pd.DataFrame(info)
    #priceDat.to_csv('PriceData.csv',encoding='utf-8')
    return priceDat

def getHistoricalDays(From,To,points,delta):
    req = requests.get('https://min-api.cryptocompare.com/data/histoday?fsym='+From+'&tsym='+To+'&limit='+points+'&aggregate='+delta+'&e=CCCAGG').json()
    info = req['Data']
    priceDat = pd.DataFrame(info)
    #priceDat.to_csv('PriceData.csv',encoding='utf-8')
    return priceDat

def getHistoricalHour(From,To,points,delta):
    req = requests.get('https://min-api.cryptocompare.com/data/histohour?fsym='+
        From+'&tsym='+To+'&limit='+points+'&aggregate='+delta+'&e=CCCAGG').json()
    
    info = req['Data']
    priceDat = pd.DataFrame(info)
    #priceDat.to_csv('PriceData.csv',encoding='utf-8')
    return priceDat

#Exchange and general coin data
# First level - 'Data'
# 'NetHashesPerSecond' - is hashes per second updated at last hour according to website
# Second level
# Data - 'AggregatedData', 'Algorithm', 'BlockNumber', 'BlockReward', 'Exchanges', 'NetHashesPerSecond'
# 'Exchanges' - listed numerically - call len()
def CoinSnapshot(coin, denominator = 'USD'):
    json = requests.get('https://www.cryptocompare.com/api/data/coinsnapshot/?fsym='+
        coin+'&tsym='+denominator).json()
    return json

# Returns data from individual exchanges
def ExchangeData(coin, denominator = 'USD'):
    json = CoinSnapshot(coin, denominator)
    ExchangeData = json['Data']['Exchanges']
    return ExchangeData

#Heiarchy
# Data - CodeRepository, CryptoCompare, Facebook, General, Reddit, Twitter
# Points - 25/Post 10/Comment 25/Follower
class SocialData:
    def __init__(self, ticker):
        ID = getID(ticker)
        json = requests.get('https://www.cryptocompare.com/api/data/socialstats/?id='+ID).json()
        # Repo may include multiple github links
        self.Repo = json['Data']['CodeRepository']['List']
        self.Facebook = json['Data']['Facebook']
        self.CCrating = json['Data']['General']
        self.Reddit = json['Data']['Reddit']
        self.Twitter = json['Data']['Twitter']
        self.all = json





if __name__ == '__main__':
    #how to pretty print json
    #rawjson = foo()
    #print json.dumps(rawjson, indent = 4, sort_keys = True)

    x = ExchangeData('ETH')
    for i in x:
        print i['MARKET']
    #p = len(x['Data']['Exchanges'])
    #p = requests.get('https://www.cryptocompare.com/api/data/socialstats/?id='+getID('ETH')).json()
    p = x
    print json.dumps(p , indent = 4, sort_keys = True)




