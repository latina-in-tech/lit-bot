from dependencies.db import SessionLocal
from models.user_role.user_role import UserRole
from sqlalchemy import ScalarResult, Select, select


async def retrieve_user_roles():
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        sql_statement: Select = select(UserRole) \
                                .order_by(UserRole.name)
            
        user_roles: ScalarResult | None = [user_role for user_role in db_session.scalars(sql_statement)]

        return user_roles if user_roles else None
    

async def retrieve_user_role_by_name(user_role_name: str) -> UserRole | None:
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Get the user role id from its name
        sql_statement: Select = select(UserRole) \
                                .where(UserRole.name == user_role_name)
            
        query_result: ScalarResult | None = db_session.scalar(sql_statement)

        return query_result if query_result else None