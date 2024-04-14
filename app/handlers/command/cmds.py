from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.utils import is_user_group_administrator
from utils.constants import BOT_COMMANDS, Emoji, ChatId


async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Message header
    message: str = f'{Emoji.TECHNOLOGIST} <b>Lista dei comandi disponibili:</b>\n'
    
    # Getting the group Administrator status of the user
    user_is_group_administrator = await is_user_group_administrator(bot=context.bot, 
                                                                    chat_id=ChatId.GENERAL,
                                                                    user_id=update.effective_chat.id)
        
    # Getting the bot commands based on the user role in the group
    commands = (BOT_COMMANDS 
                if user_is_group_administrator 
                else filter(lambda command: command['requires_admin'] == False, 
                            BOT_COMMANDS))
    
    # Compose the list of commands
    for command in commands:
        message += f'{command['name']} - {command['description']}\n'

    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
