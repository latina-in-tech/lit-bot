from models.memo.crud.delete import soft_delete_memo
from re import findall
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import ChatId, Emoji
from utils.utils import is_user_group_administrator


async def memo_pop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # If the user is not an Administrator of the Group (GENERAL Chat Id is used)
    if not await is_user_group_administrator(bot=context.bot,
                                             chat_id=ChatId.GENERAL,
                                             user_id=update.effective_user.id):
        
        await update.message.reply_text(f'{Emoji.LOCKED} Non sei abilitato a compiere quest\'azione!')
        return
    
    # Validate the user input and extract the information from the user message
    if not (matches := findall(pattern=r'^"([^"]+)"$', 
                               string=update.message.text.replace(f'/{memo_pop.__name__} ', ''))):
        await update.message.reply_text(text=f'{Emoji.WARNING} Parametri del comando non corretti.')
        return

    # Get the name of memo
    memo_name = matches[0]

    # Initialize variables
    is_memo_soft_deleted = await soft_delete_memo(memo_name=memo_name)

    # If no memo has been retrieved
    if not is_memo_soft_deleted:
        await update.effective_message.reply_text(f'Memo non trovato {Emoji.PERSON_SHRUGGING}')

        return

    # Compose the message for the user
    message = f'Memo eliminato correttamente {Emoji.CHECK_MARK_BUTTON}'
    
    await update.effective_message.reply_text(text=message, 
                                              parse_mode=ParseMode.HTML)
