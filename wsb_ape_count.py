""" functions for accessing reddit api,
    checking posts for stock symbols,
    & counting how many users are talking about a stock  """

import os
import json
import datetime as dt
from string import punctuation
import praw
from psaw import PushshiftAPI
from blacklist import BLACKLIST
import credentials as c
from services import generate_stock_list

# sets after & before in api to be the last 24hrs
TODAY = int(dt.datetime.now().timestamp())
YESTERDAY = int((dt.datetime.now() - dt.timedelta(days=1)).timestamp())


def api_start():
    """ returns gateway to reddit APIs praw & pushshift """

    reddit = praw.Reddit(
        user_agent="Comment Extraction",
        client_id=c.ID,
        client_secret=c.SECRET,
        username=c.USER,
        password=c.PASS,
    )

    api = PushshiftAPI(reddit)

    return api


def get_text(api, obj_type):
    """takes reddit/pushshift api and 'comments' or 'submissions'
    and returns a list containing the corresponding objects"""

    if obj_type == "comments":
        search_function = api.search_comments
        filters = ["author", "body"]
        check_attr = "body"
    else:  # type == "submissions"
        search_function = api.search_submissions
        filters = ["author", "title", "selftext"]
        check_attr = "selftext"

    text = list(
        search_function(
            after=YESTERDAY, before=TODAY, subreddit="wallstreetbets", filter=filters
        )
    )

    # prevent errors caused by removed/deleted posts
    text[:] = [
        x for x in text if getattr(x, check_attr) not in ("[removed]", "[deleted]")
    ]

    return text


def find_symbols(text):
    """take a text string, break it into words, check if any of them are symbols
    return a list with symbols"""

    words = text.split()
    symbols = []

    for word in words:
        # remove leading or trailing punctuation marks
        word = word.translate(str.maketrans("", "", punctuation))

        if (
            word.isalpha()
            and (word not in symbols)
            and (len(word) <= 5)
            and (word not in BLACKLIST)
            and word.isupper()
        ):
            symbols.append(word)

    return symbols


def load_symbol_list():
    """loads json list of stock symbols and
    returns function for checking if strings appear in list"""

    if not os.path.isfile("stonks.json"):
        print("generating stock list...")
        generate_stock_list()

    print("loading stocks...")
    with open("stonks.json", "r") as read_file:
        data = json.load(read_file)

    list_date = int(
        dt.datetime.strptime(data["download_time"], "%Y-%m-%d %H:%M:%S %Z").timestamp()
    )

    if TODAY - 60 * 60 * 24 * 30 > list_date:
        print("updating stock list...")
        generate_stock_list()

    def is_stock_symbol(symbol):
        if symbol in data["stonks"]:
            return True
        return False

    return is_stock_symbol


def check_texts(text, author, stonks, check_function):
    """takes a text, checks if it contains ticker symbols
    updates dict with symbol and author mentioning it
    returns updated dict"""

    tickers = find_symbols(text)
    if tickers:
        for symbol in tickers:
            if symbol in stonks.keys() and author not in stonks[symbol]:
                stonks[symbol].append(author)
            elif symbol not in stonks.keys() and check_function(symbol):
                stonks[symbol] = [author]

    return stonks


def run():
    """main program, returns dictionary of stock symbols
    and the names of the apes talking about them"""

    api = api_start()
    stonks = {}
    check_function = load_symbol_list()
    for obj in ("comments", "submissions"):
        for post in get_text(api, obj):
            if obj == "comments":
                full_text = post.body
            else:  # obj == "submissions"
                full_text = post.title + post.selftext
            try:
                stonks = check_texts(
                    full_text, post.author.name, stonks, check_function
                )
            except AttributeError:
                pass

    return stonks


def display_stonks(stonks):
    """order dictionary of stocks by number of apes mentioning them
    print out dict"""
    order = sorted(stonks, key=lambda key: len(stonks[key]), reverse=True)
    i = 0
    for symbol in order:
        if i == 12:
            break
        print(symbol, "\t", len(stonks[symbol]))
        i += 1
    return


display_stonks(run())
