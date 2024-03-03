from dependencies.db import SessionLocal
from models.job.job import Job
from models.job_category.job_category import JobCategory
from sqlalchemy import func, Result, ScalarResult, Select, select


async def retrieve_jobs() -> list[Job] | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
        
        # Select statement for the jobs' list
        select_statement: Select = select(Job) \
                                   .where(Job.deleted_at.is_(None)) \
                                   .order_by(Job.created_at.desc())
        
        # Execute the query and get the result
        query_result: ScalarResult = db_session.scalars(select_statement).all()

        return query_result if query_result else None
    

async def retrieve_job_categories() -> list[str]:

    # Variables initialization
    job_categories: list = []
    job_category_name: str = ''
    job_category_count: int = 0

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Obtain the count and the name for each job category
        sql_statement: Select = select(func.count(Job.id), JobCategory.name) \
                                .join(JobCategory, Job.job_category) \
                                .where(Job.deleted_at.is_(None)) \
                                .group_by(Job.category_id)
        
        # Executing the SELECT statement
        query_result: Result = db_session.execute(sql_statement)

        if query_result:
            
            # Compose the list for the keyboard
            for record in query_result:
                job_category_count, job_category_name = record
                job_categories.append(f'{job_category_name} ({job_category_count})')

        return job_categories
        

async def retrieve_jobs_by_category(job_category_name: str) -> list[Job] | None:
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Get the id of job category by its name
        sql_statement: Select = select(JobCategory.id) \
                                .where(JobCategory.name == job_category_name)
        
        job_category_id: int = db_session.scalar(sql_statement)

        # Get the jobs by category id
        sql_statement: Select = select(Job) \
                                .where(Job.category_id == job_category_id)
        
        query_result: list = db_session.scalars(sql_statement).all()

        return query_result if query_result else None