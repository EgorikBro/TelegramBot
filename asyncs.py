import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from dotenv import load_dotenv
from data import db_session
from data.cities import Cities
from data.stations import Stations
from api_library import *

load_dotenv()
params = {'apikey': os.getenv('APIKEY')}
flag = False


async def start(update, context):
    await update.message.reply_text("Вас приветствует бот расписаний.\n"
                                    "Что вас интересует?",
                                    reply_markup=ReplyKeyboardMarkup(
                                        [['/voyage_between_stations', '/voyage_by_station'],
                                         ['/near_station', '/near_city']]))
    return '1'


async def voyage_between_stations(update, context):
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
    if city1:
        params['from'] = city1.yandex_code
        await update.message.reply_text('Введите город прибытия.')
        return '2.1.1'
    else:
        await update.message.reply_text('Такого города нет. Повторите попытку.')
        return '2.1'


async def city_response_2(update, context):
    db_sess = db_session.create_session()
    city2 = db_sess.query(Cities).filter(Cities.city == update.message.text).first()
    if city2:
        params['to'] = city2.yandex_code
        await update.message.reply_text('Введите дату рейса в формате YYYY-MM-DD.')
        return '2.1.2'
    else:
        await update.message.reply_text('Такого города нет. Повторите попытку.')
        return '2.1.1'


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
    await update.message.reply_text('Введите количество результатов.', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def train(update, context):
    params['transport_types'] = 'train'
    await update.message.reply_text('Введите количество результатов.', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def suburban(update, context):
    params['transport_types'] = 'suburban'
    await update.message.reply_text('Введите количество результатов.', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def bus(update, context):
    params['transport_types'] = 'bus'
    await update.message.reply_text('Введите количество результатов.', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def water(update, context):
    params['transport_types'] = 'water'
    await update.message.reply_text('Введите количество результатов.', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def helicopter(update, context):
    params['transport_types'] = 'helicopter'
    await update.message.reply_text('Введите количество результатов.', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def nothing(update, context):
    await update.message.reply_text('Введите количество результатов.', reply_markup=ReplyKeyboardRemove())
    return '2.1.4'


async def number(update, context):
    global params
    n = update.message.text
    params['limit'] = n
    await update.message.reply_text('Ваши рейсы:')
    a = 1
    if params.get('from'):
        voyages = get_voyage_between(**params)
        for i in voyages['segments']:
            await update.message.reply_text(f'{a}. {i["thread"]["title"]}\n'
                                            f'Номер рейса - {i["thread"]["number"]}\n'
                                            f'Станция отправления - {i["from"]["title"]}, {i["from"]["station_type_name"]}\n'
                                            f'Станция прибытия - {i["to"]["title"]}, {i["to"]["station_type_name"]}\n'
                                            f'Время отправления - {i["departure"].split("T")[0]} {i["departure"].split("T")[1]}\n'
                                            f'Время прибытия - {i["arrival"].split("T")[0]} {i["arrival"].split("T")[1]}\n'
                                            f'Возможность приобретения электронного билета - {i["tickets_info"]["et_marker"]}\n')
            for j in i['tickets_info']['places']:
                await update.message.reply_text('Билеты:\n'
                                                f' Тип билета - {j["name"]}\n'
                                                f' Стоимость - {j["price"]["whole"] + j["price"]["cents"] / 100} {j["currency"]}\n')
            await update.message.reply_text('Информация о перевозчике:\n'
                                            f' Название - {i["thread"]["carrier"]["title"]}\n'
                                            f' Сайт - {i["thread"]["carrier"]["url"]}\n'
                                            f' Email - {i["thread"]["carrier"]["email"]}\n'
                                            f' Телефон - {i["thread"]["carrier"]["phone"]}\n"')
            a += 1
    elif params.get('station'):
        voyages = get_voyage_by_station(**params)
        for i in voyages['schedule']:
            await update.message.reply_text(f'{a}. {i["thread"]["title"]}\n'
                                            f'Номер рейса - {i["thread"]["number"]}\n'
                                            f'Время отправления - {i["departure"].split("T")[0]} {i["departure"].split("T")[1]}\n'
                                            f'Время прибытия - {i["arrival"].split("T")[0]} {i["arrival"].split("T")[1]}\n'
                                            f'Перевозчик - {i["thread"]["carrier"]["title"]}\n'
                                            f'Дни курсирования нитки: {i["days"]}\n'
                                            f'Дни, в которые нитка не курсирует: {i["except_days"]}')
            a += 1
    elif params.get('lat'):
        stations = get_stations(**params)
        for i in stations['stations']:
            await update.message.reply_text(f'{a}. {i["title"]}\n'
                                            f'Тип станции - {i["station_type_name"]}\n'
                                            f'Расстояние от вас - {round(i["distance"], 3)} км\n'
                                            f'Сайты с расписанием:')
            for j in i['type_choices']:
                await update.message.reply_text(i['type_choices'][j]['desktop_url'])
            a += 1
    await update.message.reply_text('Что ещё вас интересует?', reply_markup=ReplyKeyboardMarkup(
        [['/voyage_between_stations', '/voyage_by_station'],
         ['/near_station', '/near_city']]))
    params = {'apikey': os.getenv('APIKEY')}
    return '1'


async def station(update, context):
    await update.message.reply_text('Введите название станции отправления.',
                                    reply_markup=ReplyKeyboardRemove())
    return '2.2'


async def station_response_1(update, context):
    db_sess = db_session.create_session()
    station1 = db_sess.query(Stations).filter(Stations.station == update.message.text).first()
    if station1:
        params['from'] = station1.yandex_code
        await update.message.reply_text('Введите станцию прибытия.')
        return '2.2.1'
    else:
        await update.message.reply_text('Такой станции нет. Повторите попытку.')
        return '2.2'


async def station_response_2(update, context):
    db_sess = db_session.create_session()
    station2 = db_sess.query(Stations).filter(Stations.station == update.message.text).first()
    if station2:
        params['to'] = station2.yandex_code
        await update.message.reply_text('Введите дату рейса в формате YYYY-MM-DD.')
        return '2.1.2'
    else:
        await update.message.reply_text('Такой станции нет. Повторите попытку.')
        return '2.2.1'


async def voyage_by_station(update, context):
    await update.message.reply_text("Введите название станции.", reply_markup=ReplyKeyboardRemove())
    return '3'


async def station_response(update, context):
    db_sess = db_session.create_session()
    station1 = db_sess.query(Stations).filter(Stations.station == update.message.text).first()
    if station1:
        params['station'] = station1.yandex_code
        await update.message.reply_text('Введите дату рейса в формате YYYY-MM-DD.')
        return '2.1.2'
    else:
        await update.message.reply_text('Такой станции нет. Повторите попытку.')
        return '3'


async def near_station(update, context):
    await update.message.reply_text("Введите название объекта, от которого нужно вести поиск.",
                                    reply_markup=ReplyKeyboardRemove())
    return '4'


async def place_response(update, context):
    global flag, params
    place = update.message.text
    ll = get_ll(place)
    if ll:
        params['lat'] = ll.split()[1]
        params['lng'] = ll.split()[0]
        if not flag:
            await update.message.reply_text('Укажите радиус, в котором следует искать станции в километрах.')
            return '4.1'
        else:
            nearest_city = get_city(**params)
            await update.message.reply_text(f'Ближайший город - {nearest_city["title"]}\n'
                                            f'Расстояние до города - {round(nearest_city["distance"], 3)} км')
            await update.message.reply_text('Что ещё вас интересует?', reply_markup=ReplyKeyboardMarkup(
                                                [['/voyage_between_stations', '/voyage_by_station'],
                                                 ['/near_station', '/near_city']]))
            params = {'apikey': os.getenv('APIKEY')}
            return '1'
    else:
        await update.message.reply_text('Ошибка! Попробуйте ещё раз.')
        return '4'


async def radius_response(update, context):
    try:
        radius = int(update.message.text)
        params['distance'] = radius
        await update.message.reply_text('Выберите тип транспорта.',
                                        reply_markup=ReplyKeyboardMarkup([['/plane', '/train'],
                                                                          ['/suburban', '/bus'],
                                                                          ['/water', '/helicopter'],
                                                                          ['/nothing']]))
        return '2.1.3'
    except ValueError:
        await update.message.reply_text('Вводить нужно число!')


async def near_city(update, context):
    global flag
    flag = True
    await update.message.reply_text("Введите название объекта, от которого нужно вести поиск.",
                                    reply_markup=ReplyKeyboardRemove())
    return '4'


async def stop(update, context):
    await update.message.reply_text("До свидания!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
