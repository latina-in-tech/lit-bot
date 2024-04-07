from models.user.crud.retrieve import retrieve_users_by_role
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from utils.constants import Emoji


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # To have this MessageHandler working, the bot has to be administrator
    # in the group from which the message is gathered
    
    # If the user replied to a message
    if message_replied := update.message.reply_to_message:

        # Get the list of users which the role is Administrator
        users = await retrieve_users_by_role(role_name='Administrator')

        # Get the username of the sender and the reporter
        # In case the user has no username, the Telegram user's id is used
        sent_by = un if (un:=message_replied.from_user.username) else message_replied.from_user.id
        reported_by = un if (un:=update.message.from_user.username) else update.message.from_user.id
                
        # If there is at least an Administrator
        if users:

            message: str = (f'L\'utente @{reported_by} ha segnalato un messaggio {Emoji.POLICE_CAR_LIGHT}\n'
                            f'<b>Inviato da:</b> @{sent_by}\n'
                            f'<b>Testo del messaggio:</b>\n'
                            f'{message_replied.text}')

            await update.message.reply_text(f'Segnalazione effettuata {Emoji.POLICE_OFFICER}')

            # Send the report to every admin
            for user in users:
                
                # The chat_id is the Telegram user's id for private chats
                await context.bot.send_message(chat_id=user.telegram_id, 
                                               text=message,
                                               parse_mode=ParseMode.HTML)