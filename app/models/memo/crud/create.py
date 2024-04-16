from dependencies.db import SessionLocal
from models.memo.memo import Memo

async def create_memo(memo_data: dict) -> Memo:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Create the new memo
        memo = Memo(**memo_data)

        # Add the memo to the session
        db_session.add(memo)

        # If the memo has correctly added to the session
        if memo in db_session:
            
            # Get the memo id of the newly created memo
            memo_id = memo.id

            # Commit the transaction to the db
            db_session.commit()

            # Get the newly created memo (with all information filled up)
            # Some information like relationship(s) are not filled up until
            # the commit, so in order to get all those information,
            # we need to commit the transaction to the db and then get the
            # record with all information filled up
            return db_session.get(Memo, memo_id)
        