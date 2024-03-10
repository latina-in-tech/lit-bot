from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


COMMANDS_LIST: dict = {
    '/cmds': 'Visualizza la lista dei comandi eseguibili dal bot',
    '/contacts': 'Visualizza i contatti della LiT',
    '/create_job': 'Crea una nuova offerta di lavoro',
    '/events': 'Visualizza la lista degli eventi della community in programma',
    '/faq': 'Mostra le FAQ del gruppo',
    '/jobs': 'Visualizza la lista dei lavori proposti dai membri della community',
    '/slides': 'Visualizza il link per scaricare i template delle slides per i talk della LiT',
    '/start': 'Avvia il bot'
}

async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Compose the text to show to the user
    message: str = '<b>Lista dei comandi disponibili:</b>\n'
    message += '\n'.join([f'{k} - {v}' for k,v in COMMANDS_LIST.items()])

    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
