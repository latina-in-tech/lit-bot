from models.memo.crud.create import create_memo
from models.user.crud.create import save_user_info
from models.user.crud.retrieve import retrieve_user_by_telegram_id
from re import findall, RegexFlag
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import Character, ChatId, Emoji
from utils.utils import is_user_group_administrator


HELP_MESSAGE: str = f'{Emoji.RED_QUESTION_MARK} <b>Guida all\'utilizzo del comando /memo</b>\n' + \
                     'Crea un nuovo memo.\n\n' + \
                     f'{Emoji.TECHNOLOGIST} <b>Utilizzo</b>\n' + \
                     f'{Character.CIRCLE} fornendo i vari parametri: <code>/memo [name] [body] [?notes]</code>\n' + \
                     f'{Character.CIRCLE} rispondendo a un messaggio dell\'utente: <code>/memo [name] [?notes]</code>'

MEMO_PATTERN_WITHOUT_BODY: str = r'''^"(?P<memo_name>[^"]+)".*?
                                       (?:"(?P<memo_notes>[^"]+)")?$'''

MEMO_PATTERN_WITH_BODY: str = r'''^"(?P<memo_name>[^"]+)".*?
                                   "(?P<memo_body>[^"]+)".*?
                                    (?:"(?P<memo_notes>[^"]+)")?$'''


async def memo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # If there is any argument in the context
    if len(context.args) > 0:

        # If the first context argument is "help"
        if context.args[0] == 'help':
            await update.message.reply_text(text=HELP_MESSAGE, parse_mode=ParseMode.HTML)

            return

    # If the user is not an Administrator of the Group (GENERAL Chat Id is used)
    if not await is_user_group_administrator(bot=context.bot,
                                             chat_id=ChatId.GENERAL,
                                             user_id=update.effective_user.id):
        
        await update.message.reply_text(f'{Emoji.LOCKED} Non sei abilitato a compiere quest\'azione!')
        return 
    
    # Variables initialization
    user_telegram_id: int = update.message.from_user.id
    user_message_text: str = update.message.text.replace(f'/{memo.__name__} ', '')
    memo_data: dict = {}
    message: str = ''

    print(user_message_text)

    # Check if the user exists in the db
    if (user := await retrieve_user_by_telegram_id(user_telegram_id)):
    
        # Check if memo is getting created by replying to a message
        if (message_replied := update.message.reply_to_message):

            # Get the user who sent the message to be saved
            message_replied_user = message_replied.from_user

            # If the user doesn't exist in the db, then create it
            if not (original_poster_user := await retrieve_user_by_telegram_id(message_replied_user.id)):
                original_poster_user = await save_user_info(message_replied_user)
            
            # Save the body of the memo
            memo_data['body'] = message_replied.text

            # Check if the pattern of the command is matched, and get the matches
            if(matches := findall(pattern=MEMO_PATTERN_WITHOUT_BODY, 
                                  string=user_message_text, 
                                  flags=RegexFlag.DOTALL | RegexFlag.X)):
                
                # Matches is a list containing a tuple of matches,
                # so we take the first item in the list,
                # where the tuple of matches is present
                matches = matches[0]

                # Store the record information in the dictionary
                memo_data['name'] = matches[0]
                memo_data['notes'] = matches[1] if len(matches) == 2 else None
                memo_data['original_poster'] = original_poster_user.telegram_id

            else:
                await update.message.reply_text(text=f'{Emoji.WARNING} Parametri del comando non corretti.')
                return
        
        # Else, two to three arguments are expected (name, body and optional notes)
        elif(matches := findall(pattern=MEMO_PATTERN_WITH_BODY, 
                                string=user_message_text, 
                                flags=RegexFlag.DOTALL | RegexFlag.X)):
                
            # Matches is a list containing a tuple of matches,
            # so we take the first item in the list,
            # where the tuple of matches is present
            matches = matches[0]
            
            # Store the record information in the dictionary
            memo_data['name'], memo_data['body'] = matches[:2]
            memo_data['notes'] = matches[2] if len(matches) == 3 else None
            memo_data['original_poster'] = user.telegram_id
        else:
            await update.message.reply_text(text=f'{Emoji.WARNING} Parametri del comando non corretti.')
            return
    else:
        await update.message.reply_text(text=f'{Emoji.WARNING} Utente non trovato!')
        return
    
    # Save the id of the user who created the memo
    memo_data['created_by'] = user.id
    
    # Create the memo
    db_memo = await create_memo(memo_data=memo_data)

    # If the memo has been correctly created
    if db_memo:
    
        message = f'Memo creato correttamente {Emoji.CHECK_MARK_BUTTON}'
            
        await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
