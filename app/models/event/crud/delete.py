from datetime import datetime
from dependencies.db import SessionLocal
from models.event.event import Event
from sqlalchemy import Select, select
from uuid import UUID


async def soft_delete_event_by_id(event_id: UUID) -> bool:
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Query to select the Event
        sql_statement: Select = select(Event) \
                                .where(Event.id == event_id)

        # Select the Event
        event = db_session.scalar(sql_statement)

        # If the Event has been found,
        # update its deleted_at column and commit
        if event:
            event.deleted_at = datetime.now()
            db_session.add(event)
            db_session.commit()

            return True
        
        return False
            