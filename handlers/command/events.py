from models.event.crud.retrieve import retrieve_events
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


HELP_MESSAGE: str = '''\U00002753 <b>Guida all'utilizzo del comando /events</b>
Visualizza la lista degli eventi della community in programma.
'''


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # If there is any argument in the context
    if len(context.args) > 0:

        # If the first context argument is "help"
        if context.args[0] == 'help':
            await update.message.reply_text(text=HELP_MESSAGE, parse_mode=ParseMode.HTML)

            return
        
    # Variables initialization
    events_count: int = 0
    text: str = ''

    # Get events' list
    events_list = await retrieve_events()

    # If at least an event has been found
    if events_list:
        
        # Get the records' count
        events_count = len(events_list)
    
        # Set the text to display to the user
        text = f'\U000025b6 Numero totale di eventi: {events_count}\n'

        # Compose the list of events
        for i, event in enumerate(events_list):
            text += f'{i + 1}. <a href="{event.link}">{event.name}</a> - ' \
                    f'{datetime.strftime(event.date, '%d/%m/%Y %H:%M:%S')}\n'
                
        # Send the message to the user
        await update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text='Nessun evento trovato!')
