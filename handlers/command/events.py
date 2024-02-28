from dependencies.db import Session, get_db
from models.event.event import Event
from datetime import datetime
from sqlalchemy import Select, ScalarResult, select
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session: Session = get_db()):

    events_count: int = 0
    text: str = ''

    select_statement: Select = select(Event) \
                               .where(Event.deleted_at.is_(None)) \
                               .order_by(Event.date)
    
    query_result: ScalarResult = db_session.scalars(select_statement).all()

    if query_result:
        events_count = len(query_result)

        if events_count:
            text = f'\U000025b6 Numero totale di eventi: {events_count}\n'

            for i, event in enumerate(query_result):
                text += f'{i + 1}. <a href="{event.link}">{event.name}</a> - ' \
                        f'{datetime.strftime(event.date, '%d/%m/%Y %H:%M:%S')}\n'
                    
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Nessun evento trovato!')

        return