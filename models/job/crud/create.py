from dependencies.db import SessionLocal
from models.job.job import Job


async def create_job(job_data: dict) -> bool:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Create the new job
        job: Job = Job(**job_data)

        # Add the job to the session
        db_session.add(job)
        
        # If the job has correctly added to the session
        if job in db_session:
            db_session.commit()
            return True
        
        return False