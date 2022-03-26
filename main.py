import datetime
import os
from urllib.parse import urlparse

import tweepy
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response

app = FastAPI()


def get_twh(screen_name):
    auth = tweepy.OAuthHandler(os.getenv("TW_CK"), os.getenv("TW_CS"))
    auth.set_aaccess_token(os.getenv("TW_AT"), os.getenv("TW_AS"))
    api = tweepy.API(auth)
    uid = api.get_user(screen_name=screen_name).id
    since = (datetime.datetime.now() - datetime.timedelta(hours=-24)
             ).strftime("%Y/%m/%d_%H:%M:%S")
    twh = len(api.search_tweets(q=f"from:{screen_name} since:{since}")) / 24
    return [uid, twh]


@app.middleware("http")
async def middleware(request: Request, call_next):
    if request.method == "HEAD":
        response = Response()
    elif "herokuapp" in urlparse(str(request.url)).netloc:
        domain = os.getenv("DOMAIN")
        if domain:
            url = urlparse(str(request.url))._replace(netloc=domain).geturl()
            response = RedirectResponse(url)
        else:
            response = await call_next(request)
    else:
        response = await call_next(request)
    return response


@app.get("/")
async def get_root(request: Request):
    return {"message": "hello, world"}
