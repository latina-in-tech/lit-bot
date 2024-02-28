from collections import OrderedDict
from dotenv import dotenv_values
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler
from handlers.command.start import start
from handlers.command.events import events
from handlers.command.jobs import jobs
from handlers.command.cmds import cmds
from handlers.conversation.create_job.handler import create_job_handler
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
    
    cmds_handler = CommandHandler('cmds', cmds)
    application.add_handler(cmds_handler)

    # create_job_handler = ConversationHandler(
    #     entry_points=[CommandHandler("create_job", create_job)],
    #     states={
    #         CreateJob.CATEGORY_ID: [MessageHandler(filters.TEXT, callback=category_id)], # spostare tutto in un dict
    #         CreateJob.CONTRACT_TYPE: [MessageHandler(filters.TEXT, contract_type)],
    #         CreateJob.POSITION: [
    #             MessageHandler(filters.TEXT, position),
    #         ],
    #         CreateJob.DESCRIPTION: [MessageHandler(filters.TEXT, description)],
    #         CreateJob.LINK: [MessageHandler(filters.TEXT, link)],
    #         CreateJob.RAL: [MessageHandler(filters.TEXT, ral)]
    #     },
    #     fallbacks=[CommandHandler("cancel", lambda _: ConversationHandler.END)],
    # )

    create_job_handler = ConversationHandler(**create_job_handler)
    application.add_handler(create_job_handler)
    
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()

    # /create_event
    # /retrieve_event
    # /retrieve_events
    # /update_event
    # /delete_event (soft-delete)

    
