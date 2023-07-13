import asyncio
import logging
import sqlite3
import time
import requests
import mtranslate
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "6087137748:AAE8U1EqbDBUdAnDXMMoyYeHUefRUeZVPPU"
MSG = "---"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


def get_word():
    url = 'https://random-word-api.herokuapp.com/word'
    response = requests.get(url)
    word = response.json()[0]
    translation = mtranslate.translate(word, 'uk')
    return translation


con = sqlite3.connect("users.db")  # connect to db
cur = con.cursor()  # cursor for db


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    global word
    player_word = message.text
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Хочу загадати слово!', callback_data='next'),
    )
    await bot.send_message(message.chat.id, f'{message.from_user.first_name} перезапустив гру. Загадайте слово і почніть гру! ', reply_markup=markup)
    word = get_word()
    print(word)

@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    global word
    player_word = message.text
    if player_word.lower() == word.lower() and player_id != message.from_user.id:
        cur.execute(f"""INSERT INTO userdb VALUES ('{message.from_user.id}','{message.from_user.first_name}', 1)""")
        con.commit()
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Хочу загадати слово!', callback_data='next'),
        )
        await bot.send_message(message.chat.id, f'{message.from_user.first_name} won! ', reply_markup=markup)
        word = get_word()
        print(word)
        for row in cur.execute("SELECT * FROM userdb"):
            print(row)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'next')
async def get_text_messages(call: types.CallbackQuery):
    global player_id
    user = call.from_user
    player_id = user.id
    markup = types.InlineKeyboardMarkup()
    data = f'view_{user.id}'
    data2 = f'change_{user.id}'
    markup.add(
        types.InlineKeyboardButton(f'{user.first_name} загадує слово!(подивитись)', callback_data=data)
    ),
    markup.add(
        types.InlineKeyboardButton('Обрати інше слово', callback_data=data2)
    )
    await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('view_'))
async def get_text_messages(call: types.CallbackQuery):
    user = call.from_user  # той хто загадує слово
    if player_id != user.id:
        player = await call.bot.get_chat(player_id)
        await call.answer(f'Слово загадує {player.first_name}')
        return
    if player_id == user.id:
        await call.answer(word)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('change_'))
async def get_text_messages(call: types.CallbackQuery):
    # print(get_text_messages)
    global word
    user = call.from_user  # той хто загадує слово
    if player_id != user.id:
        player = await call.bot.get_chat(player_id)
        await call.answer(f'Слово загадує {player.first_name}!')
        return
    if player_id == user.id:
        word = get_word()
        print(word)


def show_results():
    pass


if __name__ == '__main__':
    word = get_word()
    player_id = None
    print(word)
    executor.start_polling(dp)
