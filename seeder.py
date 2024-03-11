from app.dependencies.db import SessionLocal
from app.models.contract_type.contract_type import ContractType
from app.models.job_category.job_category import JobCategory
from app.models.user_role.user_role import UserRole


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

USER_ROLES: list = [
    'User',
    'Moderator',
    'Administrator'
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
    
    for item in USER_ROLES:
        record: dict = {'name': item}
        user_role = UserRole(**record)
        db_session.add(user_role)


    db_session.commit()
