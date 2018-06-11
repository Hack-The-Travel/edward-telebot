# -*- coding: utf-8 -*-
import telebot
import sqlite3
from conf import TOKEN, DB_NAME

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    db_connection = sqlite3.connect(DB_NAME)
    cursor = db_connection.cursor()
    cursor.execute('SELECT chat_id FROM chat where chat_id={}'.format(chat_id))
    if len(cursor.fetchall()) == 0:
        cursor.execute('INSERT INTO chat (chat_id) VALUES ({})'.format(chat_id))
        db_connection.commit()
        print('New connection:', chat_id)
    db_connection.close()
    command_help(message)


@bot.message_handler(commands=['help'])
def command_help(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        '\n'.join([
            'I can help you keep up to date with news from Russian online travel market.',
            'Add me to contacts and wait for messages...'])
    )


bot.polling()
