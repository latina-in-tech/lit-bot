from itertools import batched
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from typing import Iterable


def create_inline_keyboard(items: Iterable, 
                           num_columns: int, 
                           has_close_button: bool = True) -> InlineKeyboardMarkup:
    
    # Create the keyboard
    inline_keyboard: list = [
        [InlineKeyboardButton(text=item, callback_data=item) for item in list(batch)] 
        for batch in batched(iterable=items, n=num_columns)]
    
    # Add close button if specified
    if has_close_button:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='Chiudi \U0000274C', 
                                     callback_data='close_inline_keyboard')
            ])
        
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def create_reply_keyboard(items: Iterable, 
                          num_columns: int, 
                          has_close_button: bool = True) -> ReplyKeyboardMarkup:
    
    pass