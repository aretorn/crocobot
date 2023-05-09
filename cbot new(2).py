import time
import logging
import asyncio
import random
import sqlite3
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "6087137748:AAE8U1EqbDBUdAnDXMMoyYeHUefRUeZVPPU"
MSG = "---"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
my_dict = ['слово', 'інше', 'загадка', 'костиль']  # тут нада прикрутить якийсь словник
# написати використання таблиці з словами
used_words = []  # вже використані слова

con = sqlite3.connect("users.db")  # connect to db
cur = con.cursor()  # cursor for db


# cur.execute("CREATE TABLE userDB(UserID, Name, score)")

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    #    user_id = message.from_user.id
    user = message.from_user
    user_id = user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.reply(f"Привіт, {user_full_name}!")
    for i in range(7):
        await asyncio.sleep(60 * 60 * 24)
        await bot.send_message(user_id, MSG.format(user_name))


@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    global word
    player_word = message.text
    if player_word == word:
        cur.execute(f"""INSERT INTO userdb VALUES ('{message.from_user.id}','{message.from_user.first_name}', 1)""")
        con.commit()
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('Хочу загадати слово!', callback_data='next'),
            # types.InlineKeyboardButton('Подивитись слово', callback_data='view'),
        )
        await bot.send_message(message.chat.id, f'{message.from_user.first_name} won! ', reply_markup=markup)
        word = change_word()

        print(word)
        for row in cur.execute("SELECT * FROM userdb"):
            print(row)
   #перевірка на те шо слова які вгадує загадувач - ігнорити

    #message.from_user.id == user.id:
     #   pass

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'next')
async def get_text_messages(call: types.CallbackQuery):
    user = call.from_user
    markup = types.InlineKeyboardMarkup()
    data = f'view_{user.id}'
    markup.add(
        types.InlineKeyboardButton(f'{user.first_name} загадує слово!(подивитись)', callback_data=data)
    )
    await call.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('view_'))
async def get_text_messages(call: types.CallbackQuery):
    print(get_text_messages)
    user = call.from_user
    player_id = call.data.split('_')[1]
    await call.answer(word)
    if int(player_id) != user.id:
        await call.answer('fail')
        return
    if int(player_id) == user.id:
        await call.answer(word)
# якщо той хто загадує слово напише його - не робити нічого


def change_word():
    word = random.choice(my_dict)
    return word


def show_results():
    pass


if __name__ == '__main__':
    word = change_word()
    print(word)
    executor.start_polling(dp)
