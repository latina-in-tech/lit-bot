from models.user.crud.retrieve import retrieve_user_by_telegram_id, retrieve_user_by_username
from re import findall
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import ChatId, Emoji


async def get_user_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the user of a specified chat to check its status (if it has the right to invoke the command)
    chat_member = await context.bot.get_chat_member(chat_id=ChatId.GENERAL, 
                                                    user_id=update.effective_user.id)
    
    # If the user is not an Administrator
    if not chat_member.status == ChatMember.ADMINISTRATOR:
        await update.message.reply_text(f'{Emoji.locked} Non sei abilitato a compiere quest\'azione!')
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

        message = f'L\'utente @{username} ({user_telegram_id})' + \
                  f'ha il ruolo di <b>{user_role_name}</b> {Emoji.CHECK_MARK_BUTTON}'
        
        await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)

    else:
        await update.message.reply_text(text=f'{Emoji.WARNING} Utente non trovato!')
        return
