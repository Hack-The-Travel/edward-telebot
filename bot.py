# -*- coding: utf-8 -*-
import telebot
import sqlite3
import time
from conf import TOKEN, DB_NAME, ADMIN_IDS
import logging

bot = telebot.TeleBot(TOKEN)


def execute_sql(query):
    db_connection = sqlite3.connect(DB_NAME)
    cursor = db_connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    db_connection.commit()
    db_connection.close()
    return rows


def broadcast(messages):
    for message in messages:
        if message.chat.id not in ADMIN_IDS:
            continue
        if message.content_type == 'text':
            if message.text.startswith('/'):
                continue  # ignore commands
            query = 'SELECT id FROM chat ORDER BY created_at ASC LIMIT 10'
            chat_ids = execute_sql(query)
            for chat_id in chat_ids:
                bot.send_message(chat_id[0], message.text)


@bot.message_handler(commands=['subscribe'])
def command_subscribe(message):
    chat_id = message.chat.id
    query = '''INSERT OR IGNORE INTO chat (id, username, first_name, last_name, type)
               VALUES ({id}, '{username}', '{first_name}', '{last_name}', '{type}')
            '''.format(id=chat_id, username=message.chat.username, first_name=message.chat.first_name,
                       last_name=message.chat.last_name, type=message.chat.type)
    execute_sql(query)
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


if __name__ == '__main__':
    bot.set_update_listener(broadcast)
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            bot.stop_polling()
            logging.critical(e, exc_info=True)
            time.sleep(10)
