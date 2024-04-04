from models.user.crud.create import save_user_info
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import Emoji


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the user who sent the /start command
    user = update.effective_user
    
    # Update the start message
    message: str = f'Ciao {user.full_name}! {Emoji.WAVING_HAND} \n' + \
                   f'Sono il bot del gruppo Latina In Tech {Emoji.ROBOT} \n' + \
                    'Utilizza il comando /cmds per visualizzare la lista dei comandi disponibili.'


    # Send start message
    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)

    # Save user's info
    await save_user_info(telegram_user=user)