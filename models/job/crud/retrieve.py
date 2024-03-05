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
    

async def retrieve_job_categories_with_jobs_count(include_emoji: bool) -> list[str]:

    # Variables initialization
    job_categories: list = []
    job_category_name: str = ''
    job_category_count: int = 0
    button_text: str = ''

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
                button_text = f'{JOB_CATEGORIES_EMOJI.get(job_category_name, '') if include_emoji else ''}' + ' ' + \
                              f'{job_category_name} ({job_category_count})'
                button_callback_data = job_category_name
                item = {
                    'text': button_text,
                    'callback_data': button_callback_data
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