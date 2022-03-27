import datetime
import os
from urllib.parse import urlparse

import gspread
import numpy as np
import tweepy
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response, FileResponse

app = FastAPI()


def get_twh(screen_name):
    auth = tweepy.OAuthHandler(os.getenv("TW_CK"), os.getenv("TW_CS"))
    auth.set_access_token(os.getenv("TW_AT"), os.getenv("TW_AS"))
    api = tweepy.API(auth)
    utc = datetime.timezone.utc
    since = datetime.datetime.now(utc) + datetime.timedelta(hours=-24)
    cnt = 0
    esc = False
    for p in range(10):
        tws = api.user_timeline(screen_name=screen_name, count=200, page=p)
        for tw in tws:
            if tw.created_at.replace(tzinfo=utc) < since:
                esc = True
                break
            cnt += 1
        if esc:
            break
    twh = cnt / 24
    return twh


def update_value(screen_name):
    gc = gspread.service_account_from_dict(eval(os.getenv("GS_SA")))
    sheet = gc.open("twss").sheet1
    twh = get_twh(screen_name)
    if screen_name in sheet.col_values(1):
        index = sheet.col_values(1).index(screen_name)
        sheet.update_cell(index + 1, 2, twh)
    else:
        row = len(sheet.col_values(1)) + 1
        sheet.update_cell(row, 1, screen_name)
        sheet.update_cell(row, 2, twh)
    vals = [float(f) for f in sheet.col_values(2)]
    return {"ave": np.mean(vals), "std": np.std(vals), "twh": twh}


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
    return FileResponse("./template.html")


@app.get("/u/{screen_name}")
async def get_values(screen_name: str):
    return update_value(screen_name)


@app.get("/js/script.js")
async def get_js():
    return FileResponse("./js/script.js")
