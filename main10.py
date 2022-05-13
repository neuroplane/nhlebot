import hashlib
import logging
from random import random, randrange
import requests
import jmespath
import datetime
import explode
from datetime import datetime as dt
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

API_TOKEN = '5127143578:AAGoUpyjDnt9GIjDda_ZZBNYymKwUv-wtDo'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
stats_array = []
inline_objects = [
    {"type": "pga", "title": "Field. PGA", "description": "Points, Goals, Assists", "keys": ["skaterFullName", "goals"], "url": 'https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[{"property":"points","direction":"DESC"},{"property":"goals","direction":"DESC"},{"property":"assists","direction":"DESC"},{"property":"playerId","direction":"ASC"}]&start=0&limit=10&factCayenneExp=gamesPlayed>=1&cayenneExp=gameTypeId=3 and seasonId<=20212022 and seasonId>=20212022'}
    ]

def hashgen():
    gen_hash = hashlib.md5(str(dt.now()).encode()).hexdigest()
    return gen_hash


def get_nhl_stats(url):
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers)
    return response.json()["data"]


def list_items(input_list, input_keys):
    stats = ""
    stats_line = ""
    for stat in input_list:
        for key in input_keys:
            stats_line = stats_line + str(stat[key]) + "\n"
        stats = stats + stats_line
    print(stats)
    return str(stats)


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    items = []
    for item in inline_objects:
        received_stats = get_nhl_stats(item["url"])
        print(received_stats)
        item = InlineQueryResultArticle(id=hashgen(), title=item["title"],
                                        description=item["description"],
                                        input_message_content=InputTextMessageContent(
                                            list_items(received_stats, item["keys"]), parse_mode=types.ParseMode.MARKDOWN))
        items.append(item)
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)