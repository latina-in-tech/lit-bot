from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from models.user_role.crud.retrieve import retrieve_user_roles
from models.user.crud.retrieve import retrieve_users_by_role
from utils.constants import Character, Emoji


async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message: str = ('<b>Staff del gruppo</b>\n\n'
                    f'Fondatore {Emoji.PERSON_WITH_CROWN}\n'
                    f'{Character.CIRCLE} @andreacoluzzi\n\n'
                    f'Amministratori {Emoji.POLICE_OFFICER}\n')

    # Get the list of administrators
    if administrators := await retrieve_users_by_role(role_name='Administrator'):
        
        # Add the administrator to the list of staff
        for administrator in administrators:
            message += f'{Character.CIRCLE} @{administrator.username}\n'

    await update.message.reply_text(text=message, 
                                    parse_mode=ParseMode.HTML)

    