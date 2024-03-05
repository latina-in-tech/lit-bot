from itertools import batched
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes, ConversationHandler
import logging
import json
import html
import traceback


items: list[dict] = [
    {'text': '',
     'callback_data': ''}
]

def create_inline_keyboard(name: str, 
                           items: list[dict], 
                           num_columns: int, 
                           has_close_button: bool = True) -> InlineKeyboardMarkup:
    
    # Create the keyboard
    inline_keyboard: list = [
        [InlineKeyboardButton(**item) for item in list(batch)] 
        for batch in batched(iterable=items, n=num_columns)]
    
    # Add close button if not specified differently
    if has_close_button:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='Chiudi \U0000274C', 
                                     callback_data=f'{name}_close_inline_keyboard')
            ])
        
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def close_inline_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query: CallbackQuery = update.callback_query
    await query.answer()

    await query.delete_message()

    return ConversationHandler.END


def create_reply_keyboard(items: list, 
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


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    logging.error('Exception while handling an update:', exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    logging.error(message)