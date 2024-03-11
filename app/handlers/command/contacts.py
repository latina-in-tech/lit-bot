from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


LINKS: dict = {
    '\U00002197 Telegram': 'https://t.me/+UnoCoBSIPtE1OTNk',
    '\U0001F477 LinkedIn': 'https://www.linkedin.com/company/latina-in-tech/',
    '\U0001F310 GitHub': 'https://latina-in-tech.github.io/'
}


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    message: str = ''
    
    # Compose the text to show to the user
    message += ' | '.join([f'<a href="{v}">{k}</a>' for k,v in LINKS.items()])

    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
