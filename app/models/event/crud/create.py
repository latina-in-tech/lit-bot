from dependencies.db import SessionLocal
from models.event.event import Event


async def create_event(event_data: dict) -> Event | None:

    # Event info initialization
    event_info: dict = {}
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Create the event
        event = Event(**event_data)
        
        # Add the event to the db_session
        db_session.add(event)
        
        # If the event has correctly added to the session
        if event in db_session:

            # Get the event id of the newly created event
            event_id = event.id
            
            # Commit the transaction to the db
            db_session.commit()

            # Get the newly created job (with all information filled up)
            # Some information like relationship(s) are not filled up until
            # the commit, so in order to get all those information,
            # we need to commit the transaction to the db and then get the
            # record with all information filled up
            inserted_event = db_session.get(Event, event_id)

            return inserted_event
