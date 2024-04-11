import logging
import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from asyncs import *
from data import db_session

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
APIKEY = os.getenv('APIKEY')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [CommandHandler('voyage_by_date', voyage_by_date),
                CommandHandler('voyage_by_station', voyage_by_station),
                CommandHandler('near_station', near_station),
                CommandHandler('near_city', near_city)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    db_session.global_init("db/codes.db")
    application.run_polling()


if __name__ == '__main__':
    main()