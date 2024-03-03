from itertools import batched
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from typing import Iterable
from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes, ConversationHandler


def create_inline_keyboard(items: Iterable, 
                           num_columns: int, 
                           has_close_button: bool = True) -> InlineKeyboardMarkup:
    
    # Create the keyboard
    inline_keyboard: list = [
        [InlineKeyboardButton(text=item, callback_data=item) for item in list(batch)] 
        for batch in batched(iterable=items, n=num_columns)]
    
    # Add close button if not specified differently
    if has_close_button:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='Chiudi \U0000274C', 
                                     callback_data='close_inline_keyboard')
            ])
        
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def close_inline_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query: CallbackQuery = update.callback_query
    await query.answer()

    await query.delete_message()

    return ConversationHandler.END


def create_reply_keyboard(items: Iterable, 
                          num_columns: int, 
                          input_field_placeholder: str,
                          has_close_button: bool = True) -> ReplyKeyboardMarkup:
    
    reply_markup_keyboard: list = [list(batch) for batch in batched(iterable=items, n=num_columns)]
    
    # Add close button if not specified differently
    if has_close_button:
        reply_markup_keyboard.append(['Chiudi \U0000274C'])

    return ReplyKeyboardMarkup(keyboard=reply_markup_keyboard,
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder=input_field_placeholder)