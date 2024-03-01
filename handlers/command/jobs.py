from dependencies.db import SessionLocal
from models.job.job import Job
from sqlalchemy import Select, ScalarResult, select, and_
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


HELP_MESSAGE: str = '''\U00002753 <b>Guida all'utilizzo del comando /jobs</b>
Visualizza la lista dei lavori proposti dai membri della community.

\U0001F4DD Parametri (opzionali):
- <i>contract_type_id</i> (int): 1-3 
- <i>category_id</i> (int): 1-3

\U000025B6 Utilizzo dei parametri:
/jobs contract_type_id=1 category_id=2
'''


async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # If there is any argument in the context
    if len(context.args) > 0:
    
        # If the first context argument is "help"
        if context.args[0] == 'help':
            await update.message.reply_text(text=HELP_MESSAGE, parse_mode=ParseMode.HTML)

            return

    # Variables initialization
    query_parameters: dict = {}
    jobs_count: int = 0
    text: str = ''

    # Check for the presence of arguments passed to the message
    for query_parameter in context.args:

        # Get the parameter name and value
        parameter_name, parameter_value = query_parameter.split('=')
        
        # If the parameter is not in the model's columns
        if parameter_name not in Job.__dict__.keys():
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Parametro non corretto: {parameter_name}')
            return
        
        # Else, assign it to the query parameters dictionary
        query_parameters[parameter_name] = parameter_value
    
    # Get the query parameters (if they are present)
    category_id: int | None = int(query_parameters.get('category_id', 0))
    contract_type: int | None = int(query_parameters.get('contract_type_id', 0))

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Select statement for the jobs' list
        select_statement: Select = select(Job) \
                                .where(
                                    and_(
                                        True if not category_id else Job.category_id == category_id,
                                        True if not contract_type else Job.contract_type_id == contract_type,
                                        Job.deleted_at.is_(None),
                                        )
                                    ) \
                                .order_by(Job.created_at)
        
        # Execute the query and get the result
        query_result: ScalarResult = db_session.scalars(select_statement).all()

        # If the query returned some data
        if query_result:
            
            # Get the records' count
            jobs_count = len(query_result)

            # Set the text to display to the user
            text = f'\U000025b6 Numero totale di lavori: {jobs_count} - Parametri ({query_parameters}):\n'

            # Compose the list of jobs
            for i, job in enumerate(query_result):
                text += f'{i + 1}. <a href="{job.link}">{job.position}</a> - ' \
                        f'{job.job_category.name}\n'
                    
            # Send the message to the user
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Nessun lavoro trovato!')
