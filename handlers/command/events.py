from dependencies.db import Session, get_db
from models.event.event import Event
from datetime import datetime
from sqlalchemy import Select, ScalarResult, select
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session: Session = get_db()):

    # Variables initialization
    events_count: int = 0
    text: str = ''

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
