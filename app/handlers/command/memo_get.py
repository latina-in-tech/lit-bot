from models.memo.crud.retrieve import retrieve_memo_by_name
from models.user.crud.retrieve import retrieve_user_by_telegram_id
from re import findall
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import ChatId, Emoji
from utils.utils import is_user_group_administrator


HELP_MESSAGE: str = (f'''{Emoji.RED_QUESTION_MARK} <b>Guida all'utilizzo del comando /memo_get</b>
Visualizza le informazioni di un memo in base al suo nome.\n
{Emoji.TECHNOLOGIST} <b>Utilizzo</b>
<code>/memo_get "[memo_name]"</code>\n''')


async def memo_get(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
    
    # Validate the user input and extract the information from the user message
    if not (matches := findall(pattern=r'^"([^"]+)"$', string=update.message.text.replace(f'/{memo_get.__name__} ', ''))):
        await update.message.reply_text(text=f'{Emoji.WARNING} Parametri del comando non corretti.')
        return
    
    # Get the name of the memo
    memo_name = matches[0]

    # Initialize variables
    memo = await retrieve_memo_by_name(memo_name=memo_name)

    # If no memo has been retrieved
    if not memo:
        await update.effective_message.reply_text(f'Memo memo trovato {Emoji.PERSON_SHRUGGING}')

        return

    # Get the original poster (user)
    original_poster = await retrieve_user_by_telegram_id(telegram_id=memo.original_poster)

    # Compose the message containing the memo information
    message = (
        f'<b>Nome:</b> {memo.name}\n'
        f'<b>Creato da:</b> @{memo.user.username} il {memo.created_at.strftime('%d/%m/%Y %H:%M:%S')}\n'
        f'<b>Original Poster:</b> @{original_poster.username}\n'
        f'<b>Testo:</b>\n{memo.body}\n'
        f'<b>Note:</b>{f'\n{memo.notes}' if memo.notes else ' /'}\n')
    
    await update.effective_message.reply_text(text=message, 
                                              parse_mode=ParseMode.HTML)
