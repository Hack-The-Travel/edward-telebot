# -*- coding: utf-8 -*-
import telebot
import sqlite3
import time
from conf import TOKEN, DB_NAME, ADMIN_IDS
import logging

start_time = time.time()
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
        if (message.chat.id not in ADMIN_IDS
                or message.content_type != 'text'
                or message.text.startswith('/')):
            continue
        query = 'SELECT id FROM chat ORDER BY created_at ASC LIMIT 10'
        chat_ids = execute_sql(query)
        for chat_id in chat_ids:
            try:
                bot.send_message(chat_id[0], message.text)
            except telebot.apihelper.ApiException as e:
                logging.error(e)


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


@bot.message_handler(commands=['status'])
def command_status(message):
    chat_id = message.chat.id
    if chat_id in ADMIN_IDS:
        chats_number = execute_sql('SELECT count(1) from chat')[0][0]
        uptime = time.time() - start_time
        bot.send_message(
            chat_id,
            '\n'.join([
                'up {} days, {:02d}:{:02d}'.format(int(uptime//86400), int(uptime//3600), int((uptime//60)%60)),
                'Number of subscriptions: {}'.format(chats_number)
            ])
        )
    else:
        bot.send_message(chat_id, 'Everything is ok. Stay in touch.')


if __name__ == '__main__':
    bot.set_update_listener(broadcast)
    while True:
        try:
            bot.polling(none_stop=False, timeout=60)
        except Exception as e:
            bot.stop_polling()
            logging.critical(e, exc_info=True)
            time.sleep(10)
