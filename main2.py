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

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

API_TOKEN = '5346366490:AAF3Q175IlNBRAEfQFFomnVnrsgsFjr-hxw'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
statsarr = []
quotesArray = ["Цитата дня:\n\n_Вы хоккей жопой смотрите?_\n\n@garikus89"]
quotesArray1 = [{"quote":"Цитата дня:\n\n_Вы хоккей жопой смотрите?_", "author": "@garikus89"},
                {"quote":"Цитата дня:\n\n_Вы хоккей жопой смотрите?_", "author": "@garikus89"}
                ]
print(random.choice(quotesArray1)["author"])


def hashgen():
    genhash = hashlib.md5(str(dt.now()).encode()).hexdigest()
    return genhash

def random_num(maxnum):
    return randrange(0, maxnum)

@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):

    response = ""
    text = inline_query.query or 'echo'
    response = "This is a response text"
    print(inline_query.from_user.username + " " + inline_query.query)
    statarray = getattr(InputTextMessageContent(text), "message_text").split(" ", 1)
    # print(len(statarray))
    response = random.choice(quotesArray1)["quote"] + "\n" + random.choice(quotesArray1)["author"]
    articletitle = "Цитата дня"
    input_content2 = InputTextMessageContent(response, parse_mode=types.ParseMode.MARKDOWN)
    item1 = InlineQueryResultArticle(id=hashgen(), title=articletitle,
                                     input_message_content=input_content2, thumb_url="https://pacificadulthockey.com/wp-content/uploads/2018/10/Delta-Cup.png")
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item1], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)