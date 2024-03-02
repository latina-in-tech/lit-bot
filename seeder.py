from models.contract_type.contract_type import ContractType
from models.job_category.job_category import JobCategory
from dependencies.db import SessionLocal


CONTRACT_TYPES: list = [
    'Determinato',
    'Indeterminato',
    'Apprendistato',
    'Part-time',
    'Progetto'
]

JOB_CATEGORIES: list = [
    'Back-end',
    'Cybersecurity',
    'DevOps & Cloud',
    'Front-end',
    'Machine Learning & AI',
    'Mobile',
    'Quantum Computing',
    'UX-UI'
]


with SessionLocal() as db_session:

    for item in CONTRACT_TYPES:
        record: dict = {'name': item}
        contract_type = ContractType(**record)
        db_session.add(contract_type)

    for item in JOB_CATEGORIES:
        record: dict = {'name': item}
        job_category = JobCategory(**record)
        db_session.add(job_category)

    db_session.commit()
