from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


MESSAGE: str = '''
\U0001F4DA Puoi scaricare il template delle slides LiT cliccando su 
<a href="https://github.com/latina-in-tech/lit-assets/blob/main/template-presentazione/Template-Latina-in-Tech.pptx">questo</a> link:'''


async def slides(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(text=MESSAGE, parse_mode=ParseMode.HTML)
