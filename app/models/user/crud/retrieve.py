from dependencies.db import SessionLocal
from models.user.user import User
from sqlalchemy import ScalarResult, Select, select


async def retrieve_user_by_telegram_id(telegram_id: int) -> User | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Get the user from its telegram_id
        sql_statement: Select = select(User) \
                                .where(User.telegram_id == telegram_id)
        
        query_result: ScalarResult | None = db_session.scalar(sql_statement)

        return query_result if query_result else None
    

async def retrieve_user_by_username(username: str) -> User | None:
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Get the user from its username
        sql_statement: Select = select(User) \
                                .where(User.username == username)
        
        query_result: ScalarResult | None = db_session.scalar(sql_statement)

        return query_result if query_result else None