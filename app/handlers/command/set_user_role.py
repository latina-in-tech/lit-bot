from datetime import datetime
from models.user.crud.retrieve import retrieve_user_by_telegram_id, retrieve_user_by_username
from models.user.crud.update import update_user
from models.user_role.crud.retrieve import retrieve_user_role_by_name
from re import findall
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import ChatId, Emoji, Character
from utils.utils import is_user_group_administrator


HELP_MESSAGE: str = f'{Emoji.RED_QUESTION_MARK} <b>Guida all\'utilizzo del comando /set_user_role</b>\n' + \
                     'Imposta il ruolo di un utente che ha avviato almeno una volta il bot.\n\n' + \
                     f'{Emoji.TECHNOLOGIST} <b>Utilizzo</b>\n' + \
                     f'{Character.CIRCLE} fornendo username e ruolo: <code>/set_user_role [@username] [role]</code>\n' + \
                     f'{Character.CIRCLE} rispondendo a un messaggio dell\'utente: <code>/set_user_role [role]</code>' 


async def set_user_role(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # If there is any argument in the context
    if len(context.args) > 0:

        # If the first context argument is "help"
        if context.args[0] == 'help':
            await update.message.reply_text(text=HELP_MESSAGE, parse_mode=ParseMode.HTML)

            return
    
    # If the user is not an Administrator of the Group (GENERAL Chat Id is used)
    if not is_user_group_administrator(bot=context.bot,
                                       chat_id=ChatId.GENERAL,
                                       user_id=update.effective_user.id):
        
        await update.message.reply_text(f'{Emoji.LOCKED} Non sei abilitato a compiere quest\'azione!')
        return 
    
    # Variables initialization
    user_telegram_id: int = 0
    user_role_name: str = ''
    user_role_id: int = 0
    command_args: list = context.args
    command_args_count: int = len(command_args)
    message: str = ''
    
    # Check if the role is being applied by replying to a message
    if (message_replied := update.message.reply_to_message) and command_args_count == 1:
        
        # Extract the required information
        user_telegram_id = message_replied.from_user.id
        username = un if(un:=message_replied.from_user.username) else ''
        user_role_name = command_args[0]
    
    # Else, two arguments are expected (@username and role)
    elif command_args_count == 2:
        
        # Extract the required information
        username, user_role_name = context.args
        username = matches[0] if (matches:=findall(pattern='^@(.*)$', string=username)) else None 

        # If the username has the correct pattern
        if username:
            
            # Get the Telegram ID of the User
            user_telegram_id: int = user.telegram_id if (user:= await retrieve_user_by_username(username=username)) else None
            
            # If the user_telegram_id is not found
            if not user_telegram_id:
                await update.message.reply_text(f'{Emoji.WARNING} Utente non trovato!')
                return
        else:
            await update.message.reply_text(f'{Emoji.WARNING} Username non corretto!')
            return
    else:
        await update.message.reply_text(f'{Emoji.WARNING} Parametri del comando non corretti.')
        return
    

    # Check if the user exists in the db
    if(user:=await retrieve_user_by_telegram_id(user_telegram_id)):
        
        # Get the user_role_id
        user_role_id: int = user_role.id \
                            if (user_role:=await retrieve_user_role_by_name(user_role_name=user_role_name)) \
                            else None

        # If the user_role_id has been correctly evaluated
        if user_role_id:
            
            # Update the user_role_id and when the user info have been updated
            user.role_id = user_role_id
            user.updated_at = datetime.now()
            
            # Updated the user and inform about the update
            if await update_user(user):
                message = f'L\'utente @{username} ({user_telegram_id}) ' + \
                          f'ha ora il ruolo di <b>{user_role_name}</b> {Emoji.CHECK_MARK_BUTTON}'
                
                await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text(text=f'{Emoji.CROSS_MARK} Errore durante l\'aggiornamento del ruolo dell\'utente.')
        else:
            await update.message.reply_text(text=f'{Emoji.WARNING} Ruolo dell\'utente non corretto!')
            return
    else:
        await update.message.reply_text(text=f'{Emoji.WARNING} Utente non trovato!')
        return
