from models.event.crud.retrieve import retrieve_events
from datetime import datetime
from telegram import LinkPreviewOptions, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import Emojis


HELP_MESSAGE: str = f'{Emojis.red_question_mark} <b>Guida all\'utilizzo del comando /events</b>\n' + \
                     'Visualizza la lista degli eventi della community in programma.'


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # If there is any argument in the context
    if len(context.args) > 0:

        # If the first context argument is "help"
        if context.args[0] == 'help':
            await update.message.reply_text(text=HELP_MESSAGE, parse_mode=ParseMode.HTML)

            return
        
    # Variables initialization
    events_count: int = 0
    message: str = ''

    # Get events' list
    events_list = await retrieve_events()

    # If at least an event has been found
    if events_list:
        
        # Get the records' count
        events_count = len(events_list)
    
        # Set the text to display to the user
        message = f'\U000025b6 Numero totale di eventi: {events_count}\n'

        # Compose the list of events
        for i, event in enumerate(events_list):
            message += f'{i + 1}. <a href="{event.link}">{event.name}</a> - ' \
                       f'{datetime.strftime(event.date, '%d/%m/%Y')}\n'
                
        # Send the message to the user
        await update.message.reply_text(text=message, 
                                        parse_mode=ParseMode.HTML,
                                        link_preview_options=LinkPreviewOptions(is_disabled=True))
    else:
        await update.message.reply_text(text='Nessun evento trovato!')
