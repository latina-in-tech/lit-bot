from dependencies.db import SessionLocal
from models.user.user import User
from models.user.crud.retrieve import retrieve_user_by_telegram_id
from uuid import UUID
import telegram


async def save_user_info(telegram_user: telegram.User) -> User | None:

    # Check user existance
    db_user = await retrieve_user_by_telegram_id(telegram_user.id)

    # If the user already exists, then return
    if db_user:
        return None
    
    # Extract user's info to add in the users' db table
    # For convenience, every user is set with the role "User" upon creation
    user_info: dict = {
        'first_name': telegram_user.first_name,
        'last_name': telegram_user.last_name,
        'username': telegram_user.username,
        'telegram_id': telegram_user.id,
        'role_id': 1
    }
    
    # Create the user
    user = User(**user_info)

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager    
    with SessionLocal() as db_session:

        # Add the user to the session
        db_session.add(user)

        # If the user is in the session
        if user in db_session:

            # Get the user id of the newly created user
            user_id: UUID = user.id

            # Commit the transaction to the db
            db_session.commit()

            # Get the inserted use
            inserted_user: User = db_session.get(User, user_id)

            return inserted_user
        
    return None