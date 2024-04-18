import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from dotenv import load_dotenv
from data import db_session
from data.cities import Cities
from api_library import *


load_dotenv()
params = {'apikey': os.getenv('APIKEY')}


async def start(update, context):
    await update.message.reply_text("Вас приветствует бот расписаний.\n"
                                    "Что вас интересует?",
                                    reply_markup=ReplyKeyboardMarkup([['/voyage_by_date', '/voyage_by_station'],
                                                                      ['/near_station', '/near_city']]))
    return '1'


async def voyage_by_date(update, context):
    await update.message.reply_text("Вы будете вводить город или определённую станцию?",
                                    reply_markup=ReplyKeyboardMarkup([['/city', '/station']]))
    return '2'


async def city(update, context):
    await update.message.reply_text('Введите город отправления.',
                                    reply_markup=ReplyKeyboardRemove())
    return '2.1'


async def city_response_1(update, context):
    db_sess = db_session.create_session()
    city1 = db_sess.query(Cities).filter(Cities.city == update.message.text).first()
    params['from'] = city1.yandex_code
    await update.message.reply_text('Введите город прибытия.')
    return '2.1.1'


async def city_response_2(update, context):
    db_sess = db_session.create_session()
    city2 = db_sess.query(Cities).filter(Cities.city == update.message.text).first()
    params['to'] = city2.yandex_code
    await update.message.reply_text('Введите дату рейса в формате YYYY-MM-DD.')
    return '2.1.2'


async def date_response(update, context):
    date = update.message.text
    params['date'] = date
    await update.message.reply_text('Выберите тип транспорта.',
                                    reply_markup=ReplyKeyboardMarkup([['/plane', '/train'],
                                                                      ['/suburban', '/bus'],
                                                                      ['/water', '/helicopter'],
                                                                      ['/nothing']]))
    return '2.1.3'


async def plane(update, context):
    params['transport_types'] = 'plane'
    await update.message.reply_text('Сколько рейсов выдать?', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def train(update, context):
    params['transport_types'] = 'train'
    await update.message.reply_text('Сколько рейсов выдать?', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def suburban(update, context):
    params['transport_types'] = 'suburban'
    await update.message.reply_text('Сколько рейсов выдать?', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def bus(update, context):
    params['transport_types'] = 'bus'
    await update.message.reply_text('Сколько рейсов выдать?', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def water(update, context):
    params['transport_types'] = 'water'
    await update.message.reply_text('Сколько рейсов выдать?', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def helicopter(update, context):
    params['transport_types'] = 'helicopter'
    await update.message.reply_text('Сколько рейсов выдать?', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def nothing(update, context):
    await update.message.reply_text('Сколько рейсов выдать?', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def number(update, context):
    n = update.message.text
    params['limit'] = n
    voyages = get_voyage(**params)
    await update.message.reply_text('Ваши рейсы:')
    print(voyages['segments'])
    print(params)


async def station(update, context):
    await update.message.reply_text('Введите название станции отправления.')


async def voyage_by_station(update, context):
    await update.message.reply_text("Всё найдётся!")


async def near_station(update, context):
    await update.message.reply_text("Всё найдётся!")


async def near_city(update, context):
    await update.message.reply_text("Всё найдётся!")


async def stop(update, context):
    await update.message.reply_text("До свидания!")
    return ConversationHandler.END
