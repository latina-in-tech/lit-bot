from dependencies.db import Session, get_db
from models.job.job import Job
from datetime import datetime
from sqlalchemy import Select, ScalarResult, select, and_
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session: Session = get_db()):

    query_parameters: dict = {}

    for query_parameter in context.args:
        parameter_name, parameter_value = query_parameter.split('=')
        if parameter_name not in Job.__dict__.keys():
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Parametro non corretto: {parameter_name}')
            return
        
        query_parameters[parameter_name] = parameter_value
    
    category_id: int | None = int(query_parameters.get('category_id', None))
    contract_type: int | None = int(query_parameters.get('contract_type_id', None))
    
    jobs_count: int = 0
    text: str = ''

    select_statement: Select = select(Job) \
                               .where(
                                   and_(
                                       True if not category_id else Job.category_id == category_id,
                                       True if not contract_type else Job.contract_type_id == contract_type,
                                       Job.deleted_at.is_(None),
                                       )
                                ) \
                               .order_by(Job.created_at)
    
    query_result: ScalarResult = db_session.scalars(select_statement).all()

    if query_result:
        
        jobs_count = len(query_result)

        text = f'\U000025b6 Numero totale di lavori: {jobs_count} - Parametri ({query_parameters}):\n'

        for i, job in enumerate(query_result):
            text += f'{i + 1}. <a href="{job.link}">{job.position}</a> - ' \
                    f'{job.job_category.name}\n'
                
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Nessun lavoro trovato!')

        return