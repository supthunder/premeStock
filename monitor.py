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
import random
from slackclient import SlackClient

# Use masterStock and insert ID's to monitor
IDs = {'170462':'Denim Logo Chore Coat','170471':'Supreme/LACOSTE Track Jacket','170474':'Supreme/LACOSTE Harrington Jacket','170464':'Polka Dot S/S Shirt','170463':'Curve Logo Tee','170469':'Supreme/LACOSTE L/S Jersey Polo','170473':'Supreme/LACOSTE Tennis Sweater','170465':'666 Zip Up Sweat','170466':'Sequin Logo Hooded Sweatshirt','170468':'Supreme/LACOSTE Pique Crewneck','170472':'Supreme/LACOSTE Track Pant','170470':'Supreme/LACOSTE Pique Short','170460':'Leather Camp Cap','170461':'Skew Nylon 5-Panel','170467':'Supreme/LACOSTE Pique Camp Cap','170459':'Studded Belt'}
# IDs = {'170470':'Skew Nylon 5-Panel'}

# Get this from proxies.txt
proxyList = [""]

sizeKey = ['OS','SMALL','MEDIUM','LARGE','XLARGE','S/M','L/XL','30','32','34','36',"None"]

stock = {}


def slackMsg(item,color,link, size):
    # line 101
    slack_token = ""

    if slack_token == "":
        return
    sc = SlackClient(slack_token)

    text = item+"\n"
    text += color+'\n'
    text += size.title()+'\n'
    text += link+'\n'
    text += "Restock!"+'\n'
    text += str(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3])

    sc.api_call(
      "chat.postMessage",
      channel="#test",
      text=text
    )


def sendTweet(item,color,link, size):
    # line 102
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    tweet = item+"\n"
    tweet += color+'\n'
    tweet += size.title()+'\n'
    tweet += link+'\n'
    tweet += "Restock!"+'\n'
    tweet += str(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3])

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
    global sizeKey
    with open("stock.txt", 'r') as outfile:
        oldStock = json.load(outfile)

    # For testing:
    # stock['170423']['Peach'][1] = 1
    # stock['170427']['Peach']['sizes']['LARGE'] = 0
    # stock['170462']['Red']['sizes']['MEDIUM'] = 1
    # stock['170467']["Light Pink"]['sizes']["OS"] = 1
    # print(stock['170467']["Kelly Green"]['sizes'])
    change = 0
    for ID in IDs.keys():
        try:
            for color in stock[ID]:
                for size in stock[ID][color]['sizes']:
                    if (stock[ID][color]['sizes'][size] == 1) and (oldStock[ID][color]['sizes'][size] == 0):
                        item = IDs[ID]
                        itemColor = stock[ID][color]['id']
                        link = "http://www.supremenewyork.com/shop/"+"supszn/"+str(ID)+"/"+str(itemColor)
                        itemSize = size

                        sendTweet(item,color,link, itemSize)
                        slackMsg(item,color,link, itemSize)

                        with open("stock.txt", 'w') as outfile:
                            json.dump(stock, outfile, indent=4, sort_keys=True)

                    elif (stock[ID][color]['sizes'][size] == 0) and (oldStock[ID][color]['sizes'][size] == 1):
                        stock[ID][color]['sizes'][size] = 2
                        with open("stock.txt", 'w') as outfile:
                            json.dump(stock, outfile, indent=4, sort_keys=True)


                    if (oldStock[ID][color]['sizes'][size] > 1):
                            stock[ID][color]['sizes'][size] = oldStock[ID][color]['sizes'][size] + 1
                            cprint(ID+" - OOS! ++ "+str(stock[ID][color]['sizes'][size]),"yellow")
                            with open("stock.txt", 'w') as outfile:
                                json.dump(stock, outfile, indent=4, sort_keys=True)

                    if (oldStock[ID][color]['sizes'][size] == 300):
                            print("OOS! MAX ")
                            stock[ID][color]['sizes'][size] = 0
                            cprint(IDs[ID],"red")
                            cprint("OOS","red")
                            change = 1
        except:
            print(ID)
            print(oldStock[ID][color]['sizes'])
            cprint("Invalid ID","red")


    if change == 1:
        with open("stock.txt", 'w') as outfile:
            json.dump(stock, outfile, indent=4, sort_keys=True)
    if change == 0:
        cprint("No changes!","green",attrs=['bold'])

def restockCheck(sku, extra):
    global proxyList
    global stock
    global sizeKey

    urlJson = "http://www.supremenewyork.com/shop/" + str(sku) +".json"
    user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}

    success = False
    count = 0
    while not success:
        ip = proxyList[count]

        if count == 0:
            ip = proxyList[random.randint(0,(len(proxyList) - 1))]

        proxies = {
          'http': ip,
          'https': ip
        }
        try:
            cprint("Loading proxy: {}".format(ip),"blue")
            r2 = requests.get(urlJson, headers=user, proxies=proxies, timeout=2)
            newStock = json.loads(r2.text)
            success = True
            break # just incase lol
        except:
            cprint("Banned ::: "+ip,"red")
            count += 1
            if count == (len(proxyList) - 1):
                exit()


    colorDict = {}
    for color in newStock['styles']:
        url = "http://www.supremenewyork.com/shop/" "sup/"+ str(sku) + "/" + str(color['id'])
        r = requests.get(url, headers=user, proxies=proxies, timeout=2)
        data = r.text
        soup = BeautifulSoup(data,"html.parser")

        sizeStock = {}
        sizeStock["id"] = color['id']
        stockDict = {}
        status = str(soup.find(id="add-remove-buttons"))
        if "add to cart" in status:
            # Get sizes
            sizes = soup.find(id="size")
            if sizes.find('option') == None:
                # print("OS : "+sizes.get('value'))
                stockDict['OS'] = 1
                for size in sizeKey:
                    if size not in  stockDict.keys():
                        stockDict[size] = 0
            else:
                for size in sizes.find_all('option'):
                    # print(size.text + " : " +size.get('value'))
                    stockDict[str(size.text).upper()] = 1
                for size in sizeKey:
                    if size not in  stockDict.keys():
                        stockDict[size] = 0

        elif "sold out" in status:
            stockDict['None'] = 0
            for size in sizeKey:
                # print(size.text + " : " +size.get('value'))
                stockDict[size] = 0
        sizeStock['sizes'] = stockDict

        colorDict[color['name']] = sizeStock
        # time.sleep(.15) # to not get banned

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
                json.dump(stock, outfile, indent=4, sort_keys=True)
        cprint("stock.txt saved!","green")
        exit()


    start_time = time.time()
    cprint(str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]), "magenta")
    try:
        # If you don't want threading: 
        # for ID in IDs.keys():
        #     print("Checking: {}".format(ID))
        #     restockCheck(ID, 1)
        #     time.sleep(.5)

        # Use threading:
        multiCheck(list(IDs.keys()))
        # print(stock)
        if stock:
            compareStock()
    except:
        cprint("ERROR","red", attrs=['bold'])

    cprint(str(time.time() - start_time)+" seconds", "magenta", attrs=['bold'])

if __name__ == '__main__':
    main(sys.argv)



