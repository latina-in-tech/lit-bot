from models.contract_type.contract_type import ContractType
from models.event.event import Event
from models.job.job import Job
from models.job_category.job_category import JobCategory
from datetime import datetime
from random import randint
from dependencies.db import get_db

CONTRACT_TYPES: list[dict] = [
    {'name': 'determinato'},
    {'name':'indeterminato'},
    {'name':'progetto'},
]

JOB_CATEGORIES: list[dict] = [
    {'name': 'DevOps'},
    {'name': 'IT'},
    {'name': 'Cloud'},
]

EVENTS: list[dict] = []

for i in range(1, 11):

    EVENTS.append({
        'name': f'Test event #{i}',
        'description': f'Test description event #{i}',
        'date': datetime.now(),
        'link': f'https://www.samplelink.com/event{i}',
        'created_by': randint(1, 10000)
    })

JOBS: list[dict] = []

for i in range(1, 11):

    JOBS.append({
        'contract_type_id': randint(1, 3),
        'category_id': randint(1, 3),
        'position': f'Position #{i}',
        'description': f'Test description job #{i}',
        'link': f'https://www.samplelink.com/job{i}',
        'ral': randint(20000, 50000),
        'created_by': randint(1, 10000)
    })


db_session = get_db()

for record in CONTRACT_TYPES:
    contract_type = ContractType(**record)
    db_session.add(contract_type)

for record in JOB_CATEGORIES:
    job_category = JobCategory(**record)
    db_session.add(job_category)

for record in EVENTS:
    event = Event(**record)
    db_session.add(event)

for record in JOBS:
    job = Job(**record)
    db_session.add(job)

db_session.commit()
