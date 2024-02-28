from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


COMMANDS_LIST: dict = {
    '/cmds': 'Visualizza la lista dei comandi eseguibili dal bot',
    '/events': 'Visualizza la lista degli eventi della community in programma',
    '/jobs': 'Visualizza la lista dei lavori proposti dai membri della community',
    '/start': 'Avvia il bot'
}

async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    text: str = '<b>Lista dei comandi disponibili:</b>\n'
    print([f'{k} - {v}' for k,v in COMMANDS_LIST.items()])
    text += '\n'.join([f'{k} - {v}' for k,v in COMMANDS_LIST.items()])

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
