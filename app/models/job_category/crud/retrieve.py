from dependencies.db import SessionLocal
from models.job_category.job_category import JobCategory
from sqlalchemy import ScalarResult, Select, select
from uuid import UUID


def retrieve_job_categories() -> list[JobCategory]:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Get contract types
        sql_statement: Select = select(JobCategory.name) \
                                .order_by(JobCategory.name)
            
        query_result: ScalarResult = db_session.scalars(sql_statement).all()

        return query_result if query_result else None


async def retrieve_job_category_id_by_name(job_category_name: str) -> UUID:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Get the respective contract_type_id by its name
        sql_statement: Select = select(JobCategory.id) \
                                .where(JobCategory.name == job_category_name)
        
        job_category_id: int = db_session.scalar(sql_statement)
        
        return job_category_id