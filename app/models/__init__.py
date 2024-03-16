from models.contract_type.contract_type import ContractType
from models.event.event import Event
from models.job.job import Job
from models.job_category.job_category import JobCategory
from models.user.user import User
from models.user_role.user_role import UserRole
from sqlalchemy import Text, event as sa_event, Connection, text

 
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
    'Full stack',
    'ML & AI',
    'Mobile',
    'Quantum Computing',
    'UX-UI'
]

USER_ROLES: list = [
    'User',
    'Moderator',
    'Administrator'
]


@sa_event.listens_for(ContractType.__table__, 'after_create')
def seed_contract_type_table(target, connection: Connection, **kw):

    for item in CONTRACT_TYPES:
        sql_statement: Text = text(f'INSERT INTO contract_types (name) VALUES ("{item}")')
        connection.execute(sql_statement)
    

@sa_event.listens_for(JobCategory.__table__, 'after_create')
def seed_job_category_table(target, connection: Connection, **kw):

    for item in JOB_CATEGORIES:
        sql_statement: Text = text(f'INSERT INTO job_categories (name) VALUES ("{item}")')
        connection.execute(sql_statement)


@sa_event.listens_for(UserRole.__table__, 'after_create')
def seed_user_roles_table(target, connection: Connection, **kw):

    for item in USER_ROLES:
        sql_statement: Text = text(f'INSERT INTO user_roles (name) VALUES ("{item}")')
        connection.execute(sql_statement)


