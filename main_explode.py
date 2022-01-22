import hashlib
import logging
from random import random, randrange
import requests
import jmespath
import datetime
from datetime import datetime as dt

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

API_TOKEN = '2100506147:AAGI7UjsKpUcIkkvO36Ix5O0Z3DXEXSBgOk'

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
statsarr = []


def hashgen():
    genhash = hashlib.md5(str(dt.now()).encode()).hexdigest()
    return genhash

def random_num(maxnum):
    return randrange(0, maxnum)

def get_player_stats(player):
    url = "https://api.nhle.com/stats/rest/en/skater/summary"

    querystring = {"isAggregate": "false", "isGame": "false",
                   "sort": "[{\"property\":\"points\",\"direction\":\"DESC\"},{\"property\":\"goals\",\"direction\":\"DESC\"},{\"property\":\"assists\",\"direction\":\"DESC\"},{\"property\":\"playerId\",\"direction\":\"ASC\"}]",
                   "start": "0", "limit": "50", "factCayenneExp": "gamesPlayed>=1",
                   "cayenneExp": "gameTypeId=2 and seasonId<=20212022 and seasonId>=20212022 and skaterFullName likeIgnoreCase \"%"+str(player.message_text)+"%\""}

    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring).json()

    return response

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    response = ""
    text = inline_query.query or 'echo'
    response = "This is a response text"
    statarray = getattr(InputTextMessageContent(text), "message_text").split(" ", 1)
    print(len(statarray))
    if len(statarray) < 2:
        print("Недостаточно данных")
        response = "Недостаточно данных"
    else:
        response = "Вот вам два бойца"
    input_content2 = InputTextMessageContent(response, parse_mode=types.ParseMode.MARKDOWN)
    result_id2: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(id=hashgen(), title="Item1",
                                     input_message_content=input_content2)
    item2 = InlineQueryResultArticle(id=hashgen(), title="Item2",
                                     input_message_content=input_content2)
    item3 = InlineQueryResultArticle(id=hashgen(), title="item3 from list",
                                     input_message_content=input_content2)
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item, item2, item3], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)