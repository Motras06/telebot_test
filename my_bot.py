import telebot
import time
from g4f import ChatCompletion
from telebot import types
from telebot.types import WebAppInfo
import random
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('D:\\ярик\\python_projects\\pythonProject1\\venv\\.env'))
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=["start"])
def welcome_message(message):
    if message.chat.type == 'private':
        bot.reply_to(message, f"hello {message.chat.first_name}")
    else:
        bot.reply_to(message, f"hello everyone")
    bot.send_sticker(message.chat.id,
                     sticker='CAACAgIAAxkBAAEHYNlmq8KVlodJ0_1xfRs0x1cJR1djDwAC5lIAAgMu6UinOs3OGVBnNTUE')
    time.sleep(1)
    welcome_message2(message)


def welcome_message2(message):
    lines = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = types.KeyboardButton(text="about")
    bt2 = types.KeyboardButton(text="my data")
    bt3 = types.KeyboardButton(text="random")
    bt4 = types.KeyboardButton(text="gpt")
    lines.row(bt1, bt2)
    lines.row(bt3, bt4)
    bot.send_message(message.chat.id, "What do you want to know?", reply_markup=lines)


@bot.message_handler(commands=["rezero"])
def rezero(message):
    if message.chat.type == 'private':
        lines = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lines.add(types.KeyboardButton(text="открыть", web_app=WebAppInfo(url="https://jut.su/re-zerou-kara/")))
        bot.send_sticker(message.chat.id,
                         sticker='CAACAgIAAxkBAAEHYvVmrAvbDO2E4sSH9DKdp1bFxQyb1wACHUEAAqI0sUvCqN0Uxfz9vDUE',
                         reply_markup=lines)
    else:
        bot.send_sticker(message.chat.id,
                         sticker='CAACAgIAAxkBAAEHYvVmrAvbDO2E4sSH9DKdp1bFxQyb1wACHUEAAqI0sUvCqN0Uxfz9vDUE')
        bot.send_sticker(message.chat.id,
                         sticker='CAACAgIAAxkBAAEHYvlmrA3kQ5WqbKsQF2c_YYsQ6yikhAACukAAAh_FsEsaksyFCUHONTUE')
        bot.send_sticker(message.chat.id,
                         sticker='CAACAgIAAxkBAAEHYvtmrA3yD2SoojP2gAP2Mpj6NNo66gACwEIAAtiSsUuEKJihvYnXjDUE')


def about(message):
    if message.chat.type == 'private':
        bot.reply_to(message, "about:\ndeveloper @motras_06\n"
                              "The bot is written purely to test the functionality of the Telebot library,"
                              " write to the developer about malfunctions, the bot code can be found on Github")
    else:
        bot.send_sticker(message.chat.id,
                         sticker='CAACAgIAAxkBAAEHYu9mrAqMIaeMrrORcmUG3MWoYYQDEAACV0IAAhGLsUsd6WKYEiY9sDUE')
        bot.reply_to(message, "try in private chat")


def my_data(message):
    if message.chat.type == 'private':
        bot.reply_to(message, text=f"👤Name: {message.chat.first_name}\n🆔ID: {message.chat.id}\n")
    else:
        bot.reply_to(message, text=f"👤Name of chat: {message.chat.title}\n🆔chat ID: {message.chat.id}\n")


def randomm(message):
    bot.send_message(message.chat.id, text="Inter num")
    bot.register_next_step_handler(message, random_make)


def random_make(message):
    try:
        num = message.text
        rand = random.randint(1, int(num))
        bot.send_message(message.chat.id, text=f"Your num: {str(rand)}")
    except ValueError:
        bot.send_message(message.chat.id, text="Value error")
        return randomm(message)


def gpt(message):
    line = types.ReplyKeyboardMarkup(resize_keyboard=True)
    line.add(types.KeyboardButton(text="end"))
    bot.send_message(message.chat.id, text="Inter your request", reply_markup=line)
    bot.register_next_step_handler(message, gpt_request)


def gpt_request(message):
    mess = message.text
    if mess == 'end':
        welcome_message2(message)
    else:
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.9,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["None"],
            messages=[{"role": "system", "content": ("Ты должен помогать пользователям и отвечать на все вопросы",
                                                     "Ты должен помогать пользователям")},
                      {"role": "user", "content": mess}]
        )
        bot.reply_to(message, response)
        gpt(message)


@bot.message_handler(content_types=['text'])
def on_click(message):
    mess = message.text
    if mess == 'about':
        about(message)
    elif mess == 'my data':
        my_data(message)
    elif mess == 'random':
        randomm(message)
    elif mess == 'gpt':
        gpt(message)
    else:
        if message.chat.type == 'private':
            bot.send_message(message.chat.id, text="Unreal command")
        else:
            pass


if __name__ == '__main__':
    bot.polling(non_stop=True)
