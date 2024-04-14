from itertools import batched
from telegram import (BotCommand, 
                      ChatMember, 
                      InlineKeyboardButton, 
                      InlineKeyboardMarkup, 
                      MenuButton, 
                      MenuButtonCommands, 
                      ReplyKeyboardMarkup)

from typing import Iterable
from telegram import CallbackQuery, Update
from telegram.ext import (Application, 
                          ContextTypes, 
                          ConversationHandler, 
                          ExtBot)

from utils.constants import BOT_COMMANDS, Emoji


async def post_init(application: Application):

    bot_commands: list[BotCommand] = []
        
    # Getting the bot commands based on the user role in the group
    commands = filter(lambda command: command['requires_admin'] == False, BOT_COMMANDS)
    
    # Compose the list of commands
    for command in commands:
        
        bot_command = BotCommand(command=command['name'], 
                                    description=command['description'])
        
        bot_commands.append(bot_command)

    # Set list of commands to the bot
    await application.bot.set_my_commands(commands=bot_commands)

    # Set menu button to show available bot commands
    await application.bot.set_chat_menu_button(chat_id=None, 
                                               menu_button=MenuButton(type=MenuButtonCommands.COMMANDS))
    

async def is_user_group_administrator(bot: ExtBot, chat_id: int, user_id: int) -> bool:
    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    
    return chat_member.status in [ChatMember.OWNER, ChatMember.ADMINISTRATOR]


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
                InlineKeyboardButton(text=f'Chiudi {Emoji.CROSS_MARK}', 
                                     callback_data=f'{name}_close_inline_keyboard')
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
        reply_markup_keyboard.append([f'Chiudi {Emoji.CROSS_MARK}'])

    return ReplyKeyboardMarkup(keyboard=reply_markup_keyboard,
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder=input_field_placeholder)
