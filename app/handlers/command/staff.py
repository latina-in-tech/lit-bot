from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import Character, ChatId, Emoji


async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message: str = ('<b>Staff del gruppo</b>\n\n'
                    f'Fondatore {Emoji.PERSON_WITH_CROWN}\n'
                    f'{Character.CIRCLE} @andreacoluzzi\n\n'
                    f'Amministratori {Emoji.POLICE_OFFICER}\n')

    # Get the list of the Group Telegram's Administrators
    # We are accessing the User object of the ChatMemberAdministrator
    administrators = [
        chat_member.user.username 
        for chat_member in await context.bot.get_chat_administrators(chat_id=ChatId.GENERAL)
        if (chat_member.user.is_bot == False) and (chat_member.user.username is not None)
    ]
    
    # Sort the list (it works only if there are UTF-8 characters as strings)
    administrators.sort(key=str.lower)
    
    if administrators:    
        # Add the administrator to the list of staff
        for administrator in administrators:
            message += f'{Character.CIRCLE} @{administrator}\n'

    await update.message.reply_text(text=message, 
                                    parse_mode=ParseMode.HTML)

    