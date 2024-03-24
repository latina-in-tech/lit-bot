from collections import OrderedDict
from dotenv import dotenv_values
from handlers.command.get_user_role import get_user_role
from handlers.chat_member.chat_member import on_chat_member_update
from handlers.command.start import start
from handlers.command.events import events
from handlers.command.cmds import cmds
from handlers.command.faq import faq
from handlers.command.contacts import contacts
from handlers.command.rules import rules
from handlers.command.slides import slides
from handlers.command.set_user_role import set_user_role
from handlers.conversation.create_event.handler import create_event_handler
from handlers.conversation.create_job.handler import create_job_handler
from handlers.conversation.jobs.handler import jobs_handler
from handlers.message.unknown import unknown
from handlers.conversation.easter_egg.easter_egg import easter_egg_handler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters, ChatMemberHandler
from utils.utils import error_handler
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


ENV_VARS: OrderedDict = dotenv_values('.env')
BOT_TOKEN: str = ENV_VARS['BOT_TOKEN']


if __name__ == '__main__':
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    # application.add_error_handler(error_handler)
    
    # With the filters=filters.ChatType.PRIVATE, we allow the user to invoke the command just with the bot chat,
    # This mechanism is used to avoid the user to use this command in groups
    start_handler = CommandHandler(command='start', 
                                   callback=start,
                                   filters=filters.ChatType.PRIVATE)
    application.add_handler(start_handler)
    
    cmds_handler = CommandHandler(command='cmds', 
                                  callback=cmds)
    application.add_handler(cmds_handler)
    
    contacts_handler = CommandHandler(command='contacts', 
                                      callback=contacts)
    application.add_handler(contacts_handler)

    create_job_handler = ConversationHandler(**create_job_handler)
    application.add_handler(create_job_handler)

    create_event_handler = ConversationHandler(**create_event_handler)
    application.add_handler(create_event_handler)
    
    events_handler = CommandHandler(command='events', 
                                    callback=events,
                                    filters=filters.ChatType.PRIVATE)
    application.add_handler(events_handler)

    faq_handler = CommandHandler(command='faq',
                                 callback=faq)
    application.add_handler(faq_handler)

    get_user_role_handler = CommandHandler(command='get_user_role',
                                           callback=get_user_role,
                                           filters=filters.ChatType.PRIVATE)
    application.add_handler(get_user_role_handler)
    
    jobs_handler = ConversationHandler(**jobs_handler)
    application.add_handler(jobs_handler)

    rules_handler = CommandHandler(command='rules', 
                                   callback=rules)
    application.add_handler(rules_handler)
    
    set_user_role_handler = CommandHandler(command='set_user_role', 
                                           callback=set_user_role,
                                           filters=filters.ChatType.PRIVATE)
    application.add_handler(set_user_role_handler)
    
    slides_handler = CommandHandler(command='slides', 
                                    callback=slides)
    application.add_handler(slides_handler)

    ee_handler = ConversationHandler(**easter_egg_handler)
    application.add_handler(ee_handler)

    # unknown_handler = MessageHandler(filters.COMMAND, unknown)
    # application.add_handler(unknown_handler)

    # ChatMemberHandler (use chat_member_type=MY_CHAT_MEMBER to check when the user blocks/unblocks the bot)
    # In this case, we update the user info everytime we receive an update through this handler
    chat_member_handler = ChatMemberHandler(callback=on_chat_member_update,
                                            chat_member_types=ChatMemberHandler.MY_CHAT_MEMBER)
    application.add_handler(chat_member_handler)


    # In order to use InlineKeyboard, allowed_updates=Update.ALL_TYPES must be set 
    application.run_polling(allowed_updates=Update.ALL_TYPES)
