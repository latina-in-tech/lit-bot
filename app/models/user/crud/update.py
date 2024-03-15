from dependencies.db import SessionLocal
from models.user.user import User


async def update_user(user: User) -> bool:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
        db_session.add(user)

        if user in db_session:
            db_session.commit()
            return True
        
        return False