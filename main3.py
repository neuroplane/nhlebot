import hashlib
import logging
from random import random, randrange
import requests
import jmespath
import datetime
import explode
from datetime import datetime as dt
import time
import random
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

API_TOKEN = '5127143578:AAGoUpyjDnt9GIjDda_ZZBNYymKwUv-wtDo'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

apitypes = [{}]

def hashgen():
    genhash = hashlib.md5(str(dt.now()).encode()).hexdigest()
    return genhash


def summary():
    url = "https://api.nhle.com/stats/rest/en/skater/summary"

    querystring = {"isAggregate": "false", "isGame": "false",
                   "sort": "[{\"property\":\"points\",\"direction\":\"DESC\"},{\"property\":\"goals\",\"direction\":\"DESC\"},{\"property\":\"assists\",\"direction\":\"DESC\"},{\"property\":\"playerId\",\"direction\":\"ASC\"}]",
                   "start": "0", "limit": "50", "factCayenneExp": "gamesPlayed>=1",
                   "cayenneExp": "gameTypeId=3 and seasonId<=20212022 and seasonId>=20212022"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()["data"]


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    playersarray = summary()
    print(playersarray)
    text = inline_query.query or 'echo'
    print(inline_query.from_user.username)

    items = []
    for player in playersarray:
        item = InlineQueryResultArticle(id=hashgen(), title=player["skaterFullName"] + " [" + player["teamAbbrevs"] + "]",
                                     description="P: " + str(player["points"]) + ", G: " + str(player["goals"]) + ", A: " + str(player["assists"]),
                                     input_message_content=InputTextMessageContent(
                                         player["skaterFullName"]
                                         + " [" + player["teamAbbrevs"] + "]\nTOI: "
                                         + str(player["timeOnIcePerGame"]//60) + "\nSHOTS: " + str(player["shots"]) + "\n+/-: " + str(player["plusMinus"]) + "\nPIM: " + str(player["penaltyMinutes"])),
                                     thumb_url="https://cms.nhl.bamgrid.com/images/headshots/current/168x168/" + str(player["playerId"]) + ".jpg")
        items.append(item)
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)