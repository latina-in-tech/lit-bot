from dependencies.db import SessionLocal
from models.contract_type.contract_type import ContractType
from sqlalchemy import ScalarResult, Select, select
from uuid import UUID


def retrieve_contract_types() -> list[ContractType]:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Get contract types
        sql_statement: Select = select(ContractType.name) \
                                .order_by(ContractType.name)
            
        query_result: ScalarResult = db_session.scalars(sql_statement).all()

        return query_result if query_result else None
    

async def retrieve_contract_type_id_by_name(contract_type_name: str) -> UUID:

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Get the respective contract_type_id by its name
        sql_statement: Select = select(ContractType.id) \
                                .where(ContractType.name == contract_type_name)
        
        contract_type_id: int = db_session.scalar(sql_statement)
        
        return contract_type_id
    