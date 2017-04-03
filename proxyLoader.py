import requests
from bs4 import BeautifulSoup
from OpenSSL import SSL
from termcolor import cprint
import json
import re

def filterConnections(proxiesList):
	workingProxies = []
	count = 0
	for proxy in proxiesList:
		count += 1
		cprint("Loading proxy # {}".format(count), "green")
		proxies = {
		  'http': proxy,
		  'https': proxy
		}
		try:
			r = requests.get("http://www.supremenewyork.com/shop/all", proxies=proxies, timeout=1)
			data = r.text
			soup = BeautifulSoup(data,"html.parser")
			headerCheck = str(soup.find("span",{"id":"time-zone-name"}).text)
			if headerCheck == "NYC":
				cprint(headerCheck, "blue")
				workingProxies.append(proxy)
				cprint("Added {}!".format(proxy),"green")
			else:
				cprint("Banned!", "red")
				raise
		except:
			cprint("Bad Proxy: {}".format(proxy), "red")
	return workingProxies

def site1(proxiesList):
	url = "http://www.aliveproxy.com/fastest-proxies/"
	user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
	r = requests.get(url,headers=user)

	data = r.text
	soup = BeautifulSoup(data,"html.parser")
	for ips in soup.find_all("tr",{"class":"cw-list"}):
		for ip in ips.find_all("td",{"class":"dt-tb2"}):
			print(ip)

			break;

def site2(proxiesList):
	url = "https://www.us-proxy.org/"
	user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
	r = requests.get(url,headers=user)

	data = r.text
	soup = BeautifulSoup(data,"html.parser")

	table = soup.find("tbody")
	for ips in table.find_all("tr"):
		count = 0
		proxy = ""
		for ip in ips.find_all("td"):
			if count == 0:
				proxy = str(ip.text)
				proxy += ":"
			if count == 1:
				proxy += str(ip.text)
				proxiesList.append(proxy)
				break;
			count += 1
	cprint("Succesfully added {} proxies!".format(len(proxiesList)), 'green')

def site3(proxiesList):
	url = "http://spys.ru/free-proxy-list/US/"
	user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
	
	r = requests.post(url,headers=user, data={"xpp":"1"})

	data = r.text
	soup = BeautifulSoup(data,"html.parser")

	proxy = ""
	regexProxy = "^.*(?=(document.write))"
	# for ips in soup.find_all("tr",{"class":"spy1xx"}):
	for ips in soup.find_all("tr"):
		count = 0
		for ip in ips.find_all("td",{"colspan":"1"}):
			# IP
			if count == 0:
				# rawProxy = str(ip.text)[2:20]
				proxy = str(re.sub('[a-z]','', str(ip.text)[2:20])).replace(" ","")
				if len(proxy) < 9:
					break;
			# Type:
			if count == 1:
				proxyType = str(ip.text)
				if "Squid" in proxyType:
					proxy += ":3128"
				elif "HTTPS" in proxyType:
					proxy += ":8080"
				elif "HTTP" in proxyType:
					proxy += ":80"
				elif "SOCKS5" in proxyType:
					proxy += ":1080"
				proxiesList.append(proxy)
				break;
			count += 1

	cprint("Succesfully added {} proxies!".format(len(proxiesList)), 'green')

def site4(proxiesList):
	url = "https://www.proxynova.com/proxy-server-list/country-us/"
	user = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
	
	r = requests.get(url,headers=user)
	data = r.text
	soup = BeautifulSoup(data,"html.parser")

	proxy = ""
	# for ips in soup.find_all("tr",{"class":"spy1xx"}):
	for ips in soup.find_all("tr"):
		count = 0
		for ip in ips.find_all("td",{"align":"left"}):
			if count == 0:
				proxy = str(ip.get_text(strip=True).replace("document.write('","").replace("'","").replace("+","").replace(");","").replace(" ",""))
			if count == 1:
				proxy += ":"+str(ip.text).strip()
				proxiesList.append(proxy)
				break;
			count += 1

def loadProxies():
	proxiesList = []
	cprint("Loading proxies...","green")

	site2(proxiesList) # load proxies

	# proxiesList = ["13.85.80.251:443"]
	# proxiesList = ["13.85.80.251:443"]
	# proxiesList = ["144.217.16.78:3128"]
	proxiesList = proxiesList[::-1]
	proxiesList = proxiesList[:10]
	proxiesList = filterConnections(proxiesList) # filter for working connections

	# Write to file
	with open("proxies.txt", 'w') as outfile:
		json.dump(proxiesList, outfile)
	cprint("Proxies saved to proxies.txt!","magenta","on_grey", attrs=['bold'])


loadProxies()
