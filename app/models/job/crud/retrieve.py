from dependencies.db import SessionLocal
from models.job.job import Job
from models.job_category.job_category import JobCategory
from sqlalchemy import func, Result, ScalarResult, Select, select

JOB_CATEGORIES_EMOJI: dict = {
    'Back-end': '\U0001F310',
    'Cybersecurity': '\U0001F510',
    'DevOps & Cloud': '\U00002601',
    'Front-end': '\U0001F4BB',
    'Machine Learning & AI': '\U0001F916',
    'Mobile': '\U0001F4F1',
    'Quantum Computing': '\U0000269B',
    'UX-UI': '\U0001F477'
}


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
    

async def retrieve_job_categories_with_jobs_count() -> list[dict]:

    # Variables initialization
    job_category_name: str = ''
    job_category_count: int = 0
    text: str = ''
    callback_data: str = ''
    item: dict = {}
    job_categories: list = []

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Obtain the count and the name for each job category
        sql_statement: Select = select(JobCategory.name, func.count(Job.id)) \
                                .join(JobCategory, Job.job_category) \
                                .where(Job.deleted_at.is_(None)) \
                                .group_by(Job.category_id)
        
        # Executing the SELECT statement
        query_result: Result = db_session.execute(sql_statement)

        if query_result:
            
            # Compose the list for the keyboard
            for record in query_result:
                job_category_name, job_category_count = record
                text = f'{JOB_CATEGORIES_EMOJI.get(job_category_name, '')} {job_category_name} ({job_category_count})'
                callback_data = job_category_name
                item = {
                    'text': text,
                    'callback_data': callback_data
                }

                job_categories.append(item)

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
    

def retrieve_job_category_pattern() -> str:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Getjob categories
        sql_statement: Select = select(JobCategory.name) \
                                .order_by(JobCategory.name)
        
        query_result: ScalarResult = db_session.scalars(sql_statement).all()

        if query_result:
            return f'(?:{'|'.join([job_category for job_category in query_result])})'
        
    