from dependencies.db import SessionLocal
from models.event.event import Event
from sqlalchemy import ScalarResult, Select, select


async def retrieve_events() -> list[Event] | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Select statement for the events' list
        sql_statement: Select = select(Event) \
                                .where(Event.deleted_at.is_(None)) \
                                .order_by(Event.date)
        
        # Execute the query and get the result
        query_result: ScalarResult = db_session.scalars(sql_statement).all()

        return query_result if query_result else None
