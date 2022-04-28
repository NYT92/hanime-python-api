# HaniAPI  
**Hanime API Build with Python Flask**

AND WHY not Choose THIS ONE?

- Fast API  
- Open Source
- Free To Use For Your Project
- Unrestrict Access to Some API (getVideo won't give you 1080p video)  
- Never Wasting your time building your own one
- You can MAYBE bypass cloudflare blocking If you cannot go and open the app to collect coins???  
- More API Features than The Original One:  
  - Get Comments, (Replies, Other Replies)(SOON) From Hanime Video
  - Get Landing From the front page of the Hanime.tv (SOON)
  - Authentication (*Does not support sign-up*) [Original Idea](#author--credits)
  - Collect Coins Without Clicking On Ads [Original Idea](#author--credits)
  - Checking Your Channel or Other User Channel
  - Community Upload (SOON)
  - Search
  - Request 1080p Video using X-Session-Token
  - Browse Tags & Brands
  - Get Video with Player URL and Iframe API using [nsPlayer](https://player.nscdn.ml) (*powered by playerjs*) and All Video Stream from HaniAPI (Beta) 
  
Next Update : I will try to improve code and Switching Webscraping *except : getDownloadURL* to Hanime Own API for better performance. 

# API Documentation

Move to https://haniapi-docs.vercel.app

# Running API

## REST API

From Now on, I will be switching to a new server and we will be deprecating deta.sh server in the v4, the service will be running as normal but there will be no update.

Vercel : https://hani.nsdev.ml
Railway : https://v4hani.nsdev.ml (Supported Server)  
Deta : https://v3hani.nsdev.ml (Deprecated in v4 and switch to v3hani.nsdev.ml)  

AND New Deployment will be introduce to the documentation soon...

Please Note :
*Every route get the 100 req per minute except search api get the 200 req per minute*  

## Server

If you dont want to kill your own pc, you can deploy it via these free services. Also If you want to deploy it via GCP, AWS or AZURE, I dont have a tutorial yet and you should read those cloud services docs for more info.

Deploy Via Deta.sh  

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/NYT92/hanime-python-api)

Deploy Via Railway  

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/7DfVON?referralCode=jXbUTS)

Deploy Via Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/NYT92/hanime-python-api)

## Locally

If you want to host our own api and didnt want to spend money on server, this is for you. 
No Request Limitation and Everything is free.  

*Beware of Too Too Many Requests, Hanime Server Might block the incoming request and It can be dangerous to your system but can protentially shut down Hanime Server also*  
*I am not responsible for the damage from your side*

### How to Install

*Require to Install Python 3.9+*

Clone the repo
> git clone https://github.com/NYT92/hanime-python-api.git

Install the requirements
> pip install -r requirements

Run The main.py
> python or python3 main.py

# Project / Contribute

## Project

What can you do with my api???  
Contribute this readme to add one of your project...

## Contribute

Feel Free to help me adding more feature and fixing some bug here..

# why the fuck are u doing this? it just an useless api lmaoo...

for fun n education not for something else

# Troubleshootings

If there is any problem with this API, Please make a issue report....  
ALSO  
this is for fun purposes and not for production cases.  
if you guy re from hanime staff see this pls ask nicely to remove it.  

# Author / Credits

Made with :heart_on_fire: By NYT92/nsDev from :cambodia:  
And  
- [WeaveAche/hanime-auto-coins-collector](https://github.com/WeaveAche/hanime-auto-coins-collector)  
- [Profility/hanime-scraper](https://github.com/Profility/hanime-scraper)
