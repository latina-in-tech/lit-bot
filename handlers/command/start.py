from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

START_MESSAGE: str = 'Ciao {user_full_name}! \U0001F44B\n' + \
                     'Sono il bot del gruppo Latina In Tech \U0001F916\n' + \
                     'Utilizza il comando /cmds per vedere cosa posso fare.\n' + \
                     'Per ulteriori informazioni, rivolgiti pure a un admin del gruppo \U0001F60A'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    global START_MESSAGE
    
    START_MESSAGE = START_MESSAGE.format(user_full_name=update.effective_user.full_name)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START_MESSAGE, parse_mode=ParseMode.HTML)
