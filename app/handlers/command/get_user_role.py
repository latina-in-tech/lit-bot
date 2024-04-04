from models.user.crud.retrieve import retrieve_user_by_telegram_id, retrieve_user_by_username
from re import findall
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import Character, ChatId, Emoji
from utils.utils import is_user_group_administrator


HELP_MESSAGE: str = f'{Emoji.RED_QUESTION_MARK} <b>Guida all\'utilizzo del comando /get_user_role</b>\n' + \
                     'Ottieni il ruolo di un utente che ha avviato almeno una volta il bot.\n\n' + \
                     f'{Emoji.TECHNOLOGIST} <b>Utilizzo</b>\n' + \
                     f'{Character.CIRCLE} fornendo l\'username: <code>/get_user_role [@username]</code>\n' + \
                     f'{Character.CIRCLE} rispondendo a un messaggio dell\'utente: <code>/get_user_role</code>' 


async def get_user_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
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
    command_args: list = context.args
    command_args_count: int = len(command_args)
    message: str = ''
    
    # Check if the role is getting checked by replying to a message
    if (message_replied := update.message.reply_to_message):
        
        # Extract the required information
        user_telegram_id = message_replied.from_user.id
        username = un if(un:=message_replied.from_user.username) else ''
    
    # Else, two arguments are expected (@username and role)
    elif command_args_count == 1:
        
        # Extract the required information
        username = matches[0] if (matches:=findall(pattern='^@(.*)$', string=context.args[0])) else None 

        # If the username has the correct pattern
        if username:
                
            user_telegram_id: int = user.telegram_id if (user:= await retrieve_user_by_username(username=username)) else None
            
            # If the user_telegram_id is not found
            if not user_telegram_id:
                await update.message.reply_text(f'{Emoji.WARNING} Utente non trovato!')
                return
        else:
            await update.message.reply_text(f'{Emoji.WARNING} Username non corretto!')
            return
    else:
        await update.message.reply_text(text=f'{Emoji.WARNING} Parametri del comando non corretti.')
        return
    

    # Check if the user exists in the db
    if(user:=await retrieve_user_by_telegram_id(user_telegram_id)):
        
        user_role_name: str = user.user_role.name

        message = f'L\'utente @{username} ({user_telegram_id}) ' + \
                  f'ha il ruolo di <b>{user_role_name}</b> {Emoji.CHECK_MARK_BUTTON}'
        
        await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)

    else:
        await update.message.reply_text(text=f'{Emoji.WARNING} Utente non trovato!')
        return
