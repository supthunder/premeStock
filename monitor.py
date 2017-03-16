#!/usr/bin/python3
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
import sys

# Use masterStock and insert ID's to monitor
IDs = {'170462':'Denim Logo Chore Coat','170471':'Supreme®/LACOSTE Track Jacket','170474':'Supreme®/LACOSTE Harrington Jacket','170464':'Polka Dot S/S Shirt','170463':'Curve Logo Tee','170469':'Supreme®/LACOSTE L/S Jersey Polo','170473':'Supreme®/LACOSTE Tennis Sweater','170465':'666 Zip Up Sweat','170466':'Sequin Logo Hooded Sweatshirt','170468':'Supreme®/LACOSTE Pique Crewneck','170472':'Supreme®/LACOSTE Track Pant','170470':'Supreme®/LACOSTE Pique Short','170460':'Leather Camp Cap','170461':'Skew Nylon 5-Panel','170467':'Supreme®/LACOSTE Pique Camp Cap','170459':'Studded Belt','170462':'Denim Logo Chore Coat','170471':'Supreme®/LACOSTE Track Jacket','170474':'Supreme®/LACOSTE Harrington Jacket','170464':'Polka Dot S/S Shirt','170463':'Curve Logo Tee','170469':'Supreme®/LACOSTE L/S Jersey Polo','170473':'Supreme®/LACOSTE Tennis Sweater','170465':'666 Zip Up Sweat','170466':'Sequin Logo Hooded Sweatshirt','170468':'Supreme®/LACOSTE Pique Crewneck','170472':'Supreme®/LACOSTE Track Pant','170470':'Supreme®/LACOSTE Pique Short','170460':'Leather Camp Cap','170461':'Skew Nylon 5-Panel','170467':'Supreme®/LACOSTE Pique Camp Cap','170459':'Studded Belt'}


# Get this from proxies.txt
proxyList = [""]

stock = {}

def sendTweet(item,color,link):
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
	api = tweepy.API(auth)

	tweet = item+"\n"
	tweet += color+'\n'
	tweet += link+'\n'
	tweet += "Restock!"+'\n'
	tweet += str(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3])

	try:
		# api.update_status(tweet) 
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
	try:
		with open("stock.txt", 'r') as outfile:
			oldStock = json.load(outfile)
	except:
		cprint("First run!","magenta")
		with open("stock.txt", 'w') as outfile:
			json.dump(stock, outfile)
			exit()

	# For testing:
	# stock['170423']['Peach'][1] = 1
	# stock['170423']['Light Blue'][1] = 1
	change = 0
	for ID in IDs.keys():
		try:
			for color in stock[ID]:
				if (1 in stock[ID][color]) and (1 not in oldStock[ID][color]):
					item = IDs[ID]
					link = "http://www.supremenewyork.com/#products/"+str(ID)
					sendTweet(item,color,link)
					# print("\n")
					# cprint(item,"green")
					# cprint(color,"blue")
					# cprint(link,"red")
					# print("\n")
					change = 1
				elif (1 in oldStock[ID][color]) and (1 not in stock[ID][color]):
					change = 1
					cprint(IDs[ID],"red")
					cprint("OOS","red")


		except:
			print(ID)
			cprint("Invalid ID","red")

	if change == 1:
		with open("stock.txt", 'w') as outfile:
			json.dump(stock, outfile)
	if change == 0:
		cprint("No changes!","green",attrs=['bold'])

def restockCheck(sku, extra):
	global proxyList
	global stock


	url = "http://www.supremenewyork.com/shop/" + str(sku) +".json"
	user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}

	success = False
	count = 0
	while not success:
		ip = proxyList[count]
		proxies = {
		  'http': ip,
		  'https': ip
		}
		try:
			cprint("Loading proxy: {}".format(ip),"blue")
			r = requests.get(url, headers=user, proxies=proxies, timeout=2)
			newStock = json.loads(r.text)
			success = True
			break # just incase lol
		except:
			print("excpet")
			count += 1
			if count == (len(proxyList) - 1):
				exit()



	colorDict = {}
	for color in newStock['styles']:
		sizeStock = []
		for size in color['sizes']:
			sizeStock.append(size['stock_level'])
		colorDict[color['name']] = sizeStock
	stock[sku] = colorDict

def multiCheck(items):
	with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		for item in items:
			executor.submit(restockCheck, item, 60)

def loadProxies():
	proxyList = []
	with open("proxies.txt", 'r') as outfile:
		proxyList = json.load(outfile)
	return proxyList

def main(argv):
	global IDs
	global stock

	if len(sys.argv) > 1:
		cprint("First run, saving stock.txt","green")
		for ID in IDs.keys():
			restockCheck(ID, 1)
			time.sleep(.5)

		if stock:
			with open("stock.txt", 'w') as outfile:
				json.dump(stock, outfile)
		cprint("stock.txt saved!","green")
		exit()


	start_time = time.time()
	cprint(str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]), "magenta")
	try:
		# If you don't want threading: 
		# for ID in IDs.keys():
		# 	print("Checking: {}".format(ID))
		# 	restockCheck(ID , proxy, 1)
		# 	time.sleep(.5)

		# Use threading:
		multiCheck(list(IDs.keys()))
		if stock:
			compareStock()
	except:
		cprint("ERROR","red", attrs=['bold'])

	cprint(str(time.time() - start_time)+" seconds", "magenta", attrs=['bold'])

if __name__ == '__main__':
	main(sys.argv)



