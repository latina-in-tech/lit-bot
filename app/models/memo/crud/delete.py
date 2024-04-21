from datetime import datetime
from dependencies.db import SessionLocal
from models.memo.memo import Memo
from sqlalchemy import select, Select


async def soft_delete_memo(memo_name: str) -> bool | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        sql_statement: Select = select(Memo) \
                                .where(Memo.name == memo_name)
        
        
        memo = db_session.scalar(sql_statement)
        
        if memo:
            
            memo.deleted_at = datetime.now()

            db_session.add(memo)

            db_session.commit()

            return True
        
        return False