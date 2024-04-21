from dependencies.db import SessionLocal
from models.memo.memo import Memo
from sqlalchemy import select, Select


async def retrieve_memos() -> list[Memo] | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        sql_statement: Select = select(Memo) \
                                .where(Memo.deleted_at.is_(None)) \
                                .order_by(Memo.created_at)
        
        return memos if(memos := db_session.scalars(sql_statement).unique().all()) else None
    

async def retrieve_memo_by_name(memo_name: str) -> Memo | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        sql_statement: Select = select(Memo) \
                                .where(Memo.name == memo_name)
        
        return memo if(memo := db_session.scalar(sql_statement)) else None