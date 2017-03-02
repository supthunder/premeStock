# premeStock 🤖
![Alt Text](https://zippy.gfycat.com/BabyishWelloffEasteuropeanshepherd.gif)

## What it does:
- Check for restocks
- Load free proxies
- Keep a master json of items

## Montior:
1. Create a masterstock.txt using masterStock.py
2. Find item "id" in masterstock.txt, add what you want to IDs variable in monitor.py
```python
IDs = {"170370":"Faux Fur Bomber Jacket","170399":"Field Hooded Sweatshirt","170409":"Sade Tee"}
```
3. Set tokens.py to your twitter api keys, and uncomment back "api.update_status(tweet)"
```python
try:
  # api.update_status(tweet) 
  print(tweet)
```
to:
```python
try:
  api.update_status(tweet) 
  print(tweet)
```
*first run will throw an error b/c it creates a stock.txt*

## Proxies:
1. Beta, but uses free proxies from the web, currently site2() works well
2. You get 200 proxies from site2(), however I only cycle through 10, can change value in montior.py
```python
proxyList = proxyList[:10] # I only load 10 to save time
 ```
