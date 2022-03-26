import datetime
import os
from urllib.parse import urlparse

import gspread
import tweepy
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response

app = FastAPI()


def get_twh(screen_name):
    auth = tweepy.OAuthHandler(os.getenv("TW_CK"), os.getenv("TW_CS"))
    auth.set_access_token(os.getenv("TW_AT"), os.getenv("TW_AS"))
    api = tweepy.API(auth)
    since = (datetime.datetime.now() - datetime.timedelta(hours=-24)
             ).strftime("%Y/%m/%d_%H:%M:%S")
    twh = len(api.search_tweets(q=f"from:{screen_name} since:{since}")) / 24
    return twh


def update_value(screen_name):
    gc = gspread.service_account_from_dict(eval(os.getenv("GS_SA")))
    sheet = gc.open("twss").sheet1
    twh = get_twh(screen_name)
    ave = float(sheet.cell(1, 1).value)
    cnt = int(sheet.cell(1, 2).value)
    if not sheet.cell(1, 1).value:
        sheet.update_cell(1, 1, 0)
    if not sheet.cell(1, 2).value:
        sheet.update_cell(1, 2, 0)
    if screen_name in sheet.row_values(2):
        index = sheet.row_values(2).index(screen_name)
        if not twh == float(sheet.row_values(3)[index]):
            sheet.update_cell(3, index + 1, twh)
            nave = (ave * cnt + twh) / (cnt + 1)
            sheet.update_cell(1, 1, nave)
            sheet.update_cell(1, 2, cnt + 1)
            return [nave, cnt + 1, twh]
        else:
            return [ave, cnt, twh]
    else:
        col = len(sheet.row_values(2)) + 1
        sheet.update_cell(2, col, screen_name)
        sheet.update_cell(3, col, twh)
        nave = (ave * cnt + twh) / (cnt + 1)
        sheet.update_cell(1, 1, nave)
        sheet.update_cell(1, 2, cnt + 1)
        return [nave, cnt + 1, twh]


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


@app.get("/u/{screen_name}")
async def get_values(screen_name: str):
    return update_value(screen_name)
