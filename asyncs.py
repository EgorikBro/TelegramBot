from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


params = {}


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
    await update.message.reply_text('Введите название города отправления.')


async def city_response(update, context):
    city1 = update.message.text
    params['from'] = city1


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
