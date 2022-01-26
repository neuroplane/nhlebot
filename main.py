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

API_TOKEN = '5184085257:AAHMcd122nOrN8oyKU_LEDpdqDeUtwfolVI'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
statsarr = []


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
    if len(statarray) < 2:
        # print("Недостаточно данных")
        response = "Недостаточно данных"
        articletitle = "Запрос вида @nhlelitebot player1 player2"
    else:
        response = explode.explode(statarray[0], statarray[1])
        articletitle = "Сравнить"
    input_content2 = InputTextMessageContent(response, parse_mode=types.ParseMode.MARKDOWN)
    item1 = InlineQueryResultArticle(id=hashgen(), title=articletitle,
                                     input_message_content=input_content2)
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item1], cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)