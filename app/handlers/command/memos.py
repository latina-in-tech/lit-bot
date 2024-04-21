from models.memo.crud.retrieve import retrieve_memos
from models.user.crud.retrieve import retrieve_user_by_telegram_id
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import ChatId, Emoji
from utils.utils import is_user_group_administrator


async def memos(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # If the user is not an Administrator of the Group (GENERAL Chat Id is used)
    if not await is_user_group_administrator(bot=context.bot,
                                             chat_id=ChatId.GENERAL,
                                             user_id=update.effective_user.id):
        
        await update.message.reply_text(f'{Emoji.LOCKED} Non sei abilitato a compiere quest\'azione!')
        return

    # Initialize variables
    message: str = f'<b>Lista dei Memo</b> {Emoji.MEMO}\n\n'
    memos = await retrieve_memos()

    # If no memos have been retrieved
    if not memos:
        await update.effective_message.reply_text(f'Nessun memo trovato {Emoji.PERSON_SHRUGGING}')

        return        

    # Process memos
    for memo in memos:

        # Get the original poster (user)
        original_poster = await retrieve_user_by_telegram_id(telegram_id=memo.original_poster)

        # Compose the message containing the memo information
        message += (
            f'{'-' * 101}\n'
            f'<b>Nome:</b> {memo.name}\n'
            f'<b>Creato da:</b> @{memo.user.username} il {memo.created_at.strftime('%d/%m/%Y %H:%M:%S')}\n'
            f'<b>Original Poster:</b> @{original_poster.username}\n'
            f'<b>Testo:</b>\n{memo.body}\n'
            f'<b>Note:</b>{f'\n{memo.notes}' if memo.notes else ' /'}\n')
        
    await update.effective_message.reply_text(text=message, 
                                              parse_mode=ParseMode.HTML)
