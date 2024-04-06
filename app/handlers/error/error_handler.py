from telegram import Update
from telegram.ext import ContextTypes
import logging


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    logging.error('Exception while handling an update:', exc_info=context.error)
