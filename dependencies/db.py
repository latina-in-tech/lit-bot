from models.base.base import Base
from collections import OrderedDict
from dotenv import dotenv_values
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import force_instant_defaults


ENV_VARS: OrderedDict = dotenv_values('.env')
DB_URL: str = f'{ENV_VARS['SA_DB_DIALECT']}+{ENV_VARS['SA_DB_DRIVER']}:///{ENV_VARS['SA_DB_FILEPATH']}'
              

db_engine: Engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=db_engine)
force_instant_defaults()
Base.metadata.create_all(bind=db_engine)