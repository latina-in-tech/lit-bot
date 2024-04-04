from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import EMOJIS


LINKS: dict = {
    f'{EMOJIS.up_right_arrow} Telegram': 'https://t.me/+UnoCoBSIPtE1OTNk',
    f'{EMOJIS.construction_worker} LinkedIn': 'https://www.linkedin.com/company/latina-in-tech/',
    f'{EMOJIS.globe_with_meridians} GitHub': 'https://latina-in-tech.github.io/'
}


async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    message: str = ''
    
    # Compose the text to show to the user
    message += ' | '.join([f'<a href="{v}">{k}</a>' for k,v in LINKS.items()])

    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
