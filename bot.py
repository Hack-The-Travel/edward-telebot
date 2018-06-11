# -*- coding: utf-8 -*-
import telebot
import sqlite3
from conf import TOKEN, DB_NAME

bot = telebot.TeleBot(TOKEN)


def execute_sql(query):
    db_connection = sqlite3.connect(DB_NAME)
    cursor = db_connection.cursor()
    cursor.execute(query)
    rowcount = cursor.rowcount
    db_connection.commit()
    db_connection.close()
    return rowcount


@bot.message_handler(commands=['subscribe'])
def command_subscribe(message):
    chat_id = message.chat.id
    query = '''INSERT OR IGNORE INTO chat (id, username, first_name, last_name, type)
               VALUES ({id}, '{username}', '{first_name}', '{last_name}', '{type}')
            '''.format(id=chat_id, username=message.chat.username, first_name=message.chat.first_name,
                       last_name=message.chat.last_name, type=message.chat.type)
    if execute_sql(query):
        print('New connection:', chat_id)
    bot.send_message(chat_id, 'You have been subscribed.')


@bot.message_handler(commands=['unsubscribe'])
def command_unsubscribe(message):
    chat_id = message.chat.id
    query = 'DELETE from chat where id={}'.format(chat_id)
    execute_sql(query)
    bot.send_message(chat_id, 'You have been unsubscribed.')


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
