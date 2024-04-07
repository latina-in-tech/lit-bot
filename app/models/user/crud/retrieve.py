from dependencies.db import SessionLocal
from models.user.user import User
from models.user_role.crud.retrieve import retrieve_user_role_by_name
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
    

async def check_user_role(user_telegram_id: int, user_role: str | list) -> bool | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        sql_statement: Select = select(User) \
                                .where(User.telegram_id == user_telegram_id)
        
        user: User = db_session.scalar(sql_statement)

        if isinstance(user_role, str):
            return user.user_role.name == user_role if user else None
        elif isinstance(user, list):
            return user.user_role.name in user_role if user else None
        

async def retrieve_users_by_role(role_name: str) -> list[User] | User:
    
    users: list[User] = []
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        user_role = await retrieve_user_role_by_name(user_role_name=role_name)

        sql_statement: Select = select(User) \
                                .where(User.role_id == user_role.id) \
                                .order_by(User.first_name)
        
        query_result: ScalarResult = db_session.scalars(sql_statement)

        if query_result:
            users = [user for user in query_result]

        return users