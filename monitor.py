import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import json
import tweepy
from time import gmtime, strftime
from random import randint
from datetime import datetime
from termcolor import cprint
from tokens import *

IDs = {"170370":"Faux Fur Bomber Jacket","170399":"Field Hooded Sweatshirt","170409":"Sade Tee"}
proxies = {}
stock = {}

def sendTweet(item,color,link):
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
	api = tweepy.API(auth)

	tweet = item+"\n"
	tweet += color+'\n'
	tweet += link+'\n'
	tweet += "Restock!"+'\n'
	tweet += strftime("%H:%M:%S", gmtime())

	try:
		api.update_status(tweet)
		print(tweet)
	except:
		print("Error sending tweet!")

def getIp(proxy):
	ip = proxy
	global proxies
	proxies = {
	  'http': ip,
	  'https': ip
	}

def compareStock():
	global IDs
	global stock
	with open("stock.txt", 'r') as outfile:
		oldStock = json.load(outfile)

	# stock['170370']['Red'][0] = 1
	change = 0
	for ID in IDs.keys():
		try:
			for color in stock[ID]:
				if (1 in stock[ID][color]) and (1 not in oldStock[ID][color]):
					item = IDs[ID]
					link = "http://www.supremenewyork.com/#products/"+str(ID)
					sendTweet(item,color,link)
					change = 1
				elif (1 in oldStock[ID][color]) and (1 not in stock[ID][color]):
					change = 1
					cprint(IDs[ID],"red")
					cprint("OOS","red")


		except:
			cprint("Invalid ID","red")

	if change == 1:
		with open("stock.txt", 'w') as outfile:
			json.dump(stock, outfile)
	if change == 0:
		cprint("No changes!","green",attrs=['bold'])

def restockCheck(sku, extra):
	global stock
	global proxies

	url = "http://www.supremenewyork.com/shop/" + str(sku) +".json"
	user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
	r = requests.get(url, headers=user, proxies=proxies, timeout=5)
	newStock = json.loads(r.text)

	colorDict = {}
	for color in newStock['styles']:
		sizeStock = []
		for size in color['sizes']:
			sizeStock.append(size['stock_level'])
		colorDict[color['name']] = sizeStock
	stock[sku] = colorDict


def multiCheck(items):
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
		for item in items:
			executor.submit(restockCheck, item, 60)

def loadProxies():
	proxyList = []
	with open("proxies.txt", 'r') as outfile:
		proxyList = json.load(outfile)
	return proxyList


def main():
	start_time = time.time()
	cprint(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "magenta")

	global IDs
	global stock

	proxyList = loadProxies() # Load proxies
	proxyList = proxyList[:10] # I only load 10 to save time

	IDlist = ["170370","170399","170409"] # Use masterStock and insert ID's to monitor

	for proxy in proxyList:
		cprint("Using proxy: {}".format(proxy),"blue")
		try:
			# If you don't want threading: 
			# for ID in IDs.keys():
			# 	restockCheck(ID,stock)
			# 	time.sleep(.5)

			# Use threading:
			multiCheck(list(IDs.keys()))
			if stock:
				compareStock()
			break;
		except:
			cprint("ERROR","red", attrs=['bold'])

	cprint(str(time.time() - start_time)+" seconds", "magenta", attrs=['bold'])

if __name__ == '__main__':
	main()




