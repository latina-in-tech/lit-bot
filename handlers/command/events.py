from dependencies.db import SessionLocal
from models.event.event import Event
from datetime import datetime
from sqlalchemy import Select, ScalarResult, select
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

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Select statement for the events' list
        select_statement: Select = select(Event) \
                                .where(Event.deleted_at.is_(None)) \
                                .order_by(Event.date)
        
        # Execute the query and get the result
        query_result: ScalarResult = db_session.scalars(select_statement).all()

        # If the query returned some data
        if query_result:

            # Get the records' count
            events_count = len(query_result)
        
            # Set the text to display to the user
            text = f'\U000025b6 Numero totale di eventi: {events_count}\n'

            # Compose the list of events
            for i, event in enumerate(query_result):
                text += f'{i + 1}. <a href="{event.link}">{event.name}</a> - ' \
                        f'{datetime.strftime(event.date, '%d/%m/%Y %H:%M:%S')}\n'
                    
            # Send the message to the user
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Nessun evento trovato!')
