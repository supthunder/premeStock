# premeStock 🤖
![Alt Text](https://zippy.gfycat.com/BabyishWelloffEasteuropeanshepherd.gif)

## What it does:
- Check for restocks
- Send tweet/slack msg
- Load free proxies from 4 sites

## Currently live [@supszn](https://twitter.com/supszn) running every 10 seconds

## How to run:
1. Pre-reqs: [Python3](https://www.python.org/ftp/python/3.6.1/python-3.6.1-macosx10.6.pkg), git. (Both pre-installed on osx)
2. Open terminal, clone project:

![gif](/images/first.gif)

3. (optional and beta) Create proxies (note if you use these faster than say 10s, supreme will ban you!)
**Note these are free proxies, and if it gets banned, monitor will glitch/give false alerts
![gif](/images/proxy.gif)

4. Get stock list, and filter using keywords, enter "new" to get all new items.
![gif](/images/stock.gif)

5. Load stock and proxies into monitor.py
![gif](/images/load.gif)

6. First run, use "y" to generate stock.txt: ```python monitor.py y```
![gif](/images/first.gif)

7. Done, add twitter/slack tokens to tokens.py and run ```python monitor.py```

![gif](/images/restock.gif)

![gif](/images/nochange.gif)


