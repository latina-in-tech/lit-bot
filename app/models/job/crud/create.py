from dependencies.db import SessionLocal
from models.job.job import Job


async def create_job(job_data: dict) -> dict | None:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Create the new job
        job: Job = Job(**job_data)

        # Add the job to the session
        db_session.add(job)
        
        # If the job has correctly added to the session
        if job in db_session:
            
            # Get the job id of the newly created job
            job_id = job.id
            
            # Commit the transaction to the db
            db_session.commit()

            # Get the newly created job (with all information filled up)
            # Some information like relationship(s) are not filled up until
            # the commit, so in order to get all those information,
            # we need to commit the transaction to the db and then get the
            # record with all information filled up
            inserted_job = db_session.get(Job, job_id)
            
            job_info = {
                'Tipologia di contratto': inserted_job.contract_type.name,
                'Ambito': inserted_job.job_category.name,
                'Posizione ricercata': inserted_job.position,
                'Descrizione': inserted_job.description,
                'Link dell\'offerta': inserted_job.link if inserted_job.link is not None else 'Non disponibile',
                'Compenso (annuo o totale)': f'€ {inserted_job.ral}' if inserted_job.ral is not None else 'Non disponibile'
            }

            return job_info
        
        return None