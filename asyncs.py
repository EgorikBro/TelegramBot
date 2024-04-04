from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


async def start(update, context):
    await update.message.reply_text("Вас приветствует бот расписаний.\n"
                                    "Что вас интересует?",
                                    reply_markup=ReplyKeyboardMarkup([['/voyage_by_date']]))
    return 1


async def voyage_by_date(update, context):
    await update.message.reply_text("Всё найдётся!")


async def stop(update, context):
    await update.message.reply_text("До свидания!")
    return ConversationHandler.END