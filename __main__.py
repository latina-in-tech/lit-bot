from collections import OrderedDict
from dotenv import dotenv_values
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters
from handlers.command.start import start
from handlers.command.events import events
from handlers.conversation.jobs.handler import jobs_handler
from handlers.command.cmds import cmds
from handlers.conversation.create_job.handler import create_job_handler
from handlers.message.unknown import unknown
import logging

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
    
    jobs_handler = ConversationHandler(**jobs_handler)
    application.add_handler(jobs_handler)
    
    cmds_handler = CommandHandler('cmds', cmds)
    application.add_handler(cmds_handler)

    create_job_handler = ConversationHandler(**create_job_handler)
    application.add_handler(create_job_handler)
    
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)   
