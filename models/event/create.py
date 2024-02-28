from models.event.event import Event
from datetime import datetime
from uuid import  uuid4
from sqlalchemy.orm import Session

def create_event(session: Session, event_info: dict):
    
    event_info['id'] = uuid4()
    
    event: Event = Event(**event_info)

    if event:
        session.add(event)
        session.commit()