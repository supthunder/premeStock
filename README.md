# premeStock 🤖
![Alt Text](https://zippy.gfycat.com/BabyishWelloffEasteuropeanshepherd.gif)

## What it does:
- Check for restocks
- Load free proxies
- Keep a master json of items

## How to run:
- Check [Wiki](https://github.com/supthunder/premeStock/wiki/How-to-run)

## Currently live [@supszn](https://twitter.com/supszn) running every .5 seconds
<img src="http://i.imgur.com/FgTWh3n.png" width="580">

## Montior:
1. Create a masterstock.txt using masterStock.py
2. Find item "id" in masterstock.txt, add what you want to IDs variable in monitor.py

\**This is to avoid a cluttered timeline, only monitor items you want*
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
\**first run will throw an error b/c it creates a stock.txt*

## Proxies:
1. Beta, but uses free proxies from the web, currently site2() works well
2. You get 200 proxies from site2(), however I only cycle through 10, can change value in montior.py
```python
proxyList = proxyList[:10] # I only load 10 to save time
 ```
 ![Alt Text](http://i.imgur.com/chP9k85.gif)
 
### How does it handle stock glitch?
1. Waits 1hr once restocked to prevent repeated alerts


![Alt Text](http://i.imgur.com/ymoBrlt.png)


## To do:
1. Sort proxies by delay ms
2. Check actual website vs json for stock
