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
my_dict = ['слово', 'інше', 'загадка', 'костиль'] #тут нада прикрутить якийсь словник
#написати використання таблиці з словами
used_words = [] #вже використані слова

con = sqlite3.connect("users.db") #connect to db
cur = con.cursor() #cursor for db
#cur.execute("CREATE TABLE userDB(UserID, Name, score)")

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.reply(f"Привіт, {user_full_name}!")
    for i in range(7):
       await asyncio.sleep(60*60*24)
       await bot.send_message(user_id, MSG.format(user_name))
@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
  global word
  player_word = message.text
  if player_word == word:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name} won! ')
        # записати результат в файл БД
        cur.execute("""INSERT INTO userdb VALUES (f '{message.from_user.id}','{message.from_user.first_name}', 1)""")
        con.commit()
        word = change_word()
  if message.text == "Привіт Бот!":
      await bot.send_message(message.from_user.id, "/help для допомоги")
  elif message.text == "/help":
      await bot.send_message(message.from_user.id, "Привіт! Ти зайшов в чат для гри в крокодила. Вгадуй слова, які пояснюють гравці та загадуй свлова сам, якщо вгадаєш.")
  elif message.text == "Дошка результатів":
      await bot.send_message(message.from_user.id, "Привіт! Ось результати гравців!")
      

def change_word():
    word = random.choice(my_dict)
    return word


def show_results():
    pass



if __name__ == '__main__':
    word = change_word()
    print(word)
    executor.start_polling(dp)





