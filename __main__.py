from collections import OrderedDict
from dotenv import dotenv_values
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler
from handlers.command.start import start
from handlers.command.events import events
from handlers.command.jobs import jobs
from handlers.message.unknown import unknown
import logging
from telegram.ext import filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


ENV_VARS: OrderedDict = dotenv_values('.env')
BOT_TOKEN: str = ENV_VARS['BOT_TOKEN']


if __name__ == '__main__':
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    events_handler = CommandHandler('events', events)
    application.add_handler(events_handler)

    jobs_handler = CommandHandler('jobs', jobs)
    application.add_handler(jobs_handler)
    
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()

    # /create_event
    # /retrieve_event
    # /retrieve_events
    # /update_event
    # /delete_event (soft-delete)

    
