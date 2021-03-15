# WSB Ape Counter
This program scrapes r/wallstreetbets for stock symbols and counts how many redditors are talking about them.


## Installation
1. Clone this repo
``git clone  ``

2. Install requirements
``pip install -r requirements.txt``

3. Fill out 'credentials.py' with the appropriate info. 
You'll need a Reddit account with OAuth2 for a script app, please see this page for details: <https://github.com/reddit-archive/reddit/wiki/OAuth2>

You also need an API key for <https://fcsapi.com/ >, it's free.


## Usage
``python wsb_ape_count.py``

### Sample Output:
```
GME 	 1698
AMC 	 306
RKT 	 114
PLTR 	 104
BB   	 71
TSLA 	 70
F 	     63
AAPL 	 43
NIO 	 41
RIOT 	 38
NOK 	 37
MVIS 	 34
```
the number is how many different redditors mentioned the stock symbol


## Thanks

I found Part Time Larry's [video](https://www.youtube.com/watch?v=CJAdCLZaISw) really helpful when writing this. Also these two repos: <https://github.com/asad70/wallstreetbets-sentiment-analysis> & <https://github.com/RyanElliott10/wsbtickerbot>


## Contact

dave@daveaustin.xyz