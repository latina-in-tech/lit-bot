from dependencies.db import SessionLocal
from models.job.job import Job
from models.job_category.job_category import JobCategory
from models.contract_type.contract_type import ContractType
from enum import Enum
from sqlalchemy import Select, select, Result
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, filters, MessageHandler
from itertools import batched


def create_keyboard(num_columns: int, items: list) -> list[list]:
    return [list(batch) for batch in batched(iterable=items, n=num_columns)]


# CreateJob Enum for the ConversationHandler steps
class CreateJob(Enum):
    CONTRACT_TYPE: int = 0 
    CATEGORY_ID: int = 1
    POSITION: int = 2
    DESCRIPTION: int = 3
    LINK: int = 4
    RAL: int = 5

# Initialize an empty dict for the new job's data
job_data: dict = {}

with SessionLocal() as db_session:

    # Get contract types
    sql_statement: Select = select(ContractType.name) \
                            .order_by(ContractType.name)
        
    query_result: Result = db_session.execute(sql_statement).all()

    if query_result:
        contract_types: list = [record[0] for record in query_result] 

        # Keyboard
        # Each row is a list, and each button is an item
        # On each row there are four buttons
        contract_types_reply_keyboard: list = create_keyboard(num_columns=3, items=contract_types)
        
        # Filter pattern
        contract_types_filter_pattern: str = f'^({'|'.join(contract_types)})$'

    # Get job categories
    sql_statement: Select = select(JobCategory.name) \
                            .order_by(JobCategory.name)

    query_result: Result = db_session.execute(sql_statement).all()

    if query_result:
        job_categories: list = [record[0] for record in query_result] 

        # Keyboard
        job_categories_reply_keyboard = create_keyboard(num_columns=2, items=job_categories)
        
        # Filter pattern
        category_ids_filter_pattern = f'^({'|'.join(job_categories)})$'


async def create_job(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    
    # Set the text to be displayed as hint in the text input field
    input_field_placeholder: str = 'Seleziona la tipologia di contratto del lavoro dal menu sottostante:'
    
    await update.message.reply_text('Seleziona la tipologia di contratto \U0001F4DD',
                                    reply_markup=ReplyKeyboardMarkup(
                                    keyboard=contract_types_reply_keyboard, 
                                    one_time_keyboard=True,
                                    input_field_placeholder=input_field_placeholder,
                                    resize_keyboard=True))

    return CreateJob.CONTRACT_TYPE


async def validate_contract_type(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Set the text to be displayed as hint in the text input field
    input_field_placeholder: str = 'Seleziona la tipologia di contratto del lavoro dal menu sottostante:'
    
    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'La scelta inserita non e\' valida.\n' + \
                                    'Seleziona la tipologia di contratto:',
                                    reply_markup=ReplyKeyboardMarkup(
                                    keyboard=contract_types_reply_keyboard, 
                                    one_time_keyboard=True,
                                    input_field_placeholder=input_field_placeholder,
                                    resize_keyboard=True))
    
    return CreateJob.CONTRACT_TYPE


async def contract_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the contract_type_id (that here is string corresponding to the "name" column) of the contract_type
    job_data['contract_type_id'] = user_message

    # Set the text to be displayed as hint in the text input field
    input_field_placeholder: str = 'Seleziona la categoria del lavoro dal menu sottostante:'

    await update.message.reply_text('Seleziona la categoria \U0001F520',
                                    reply_markup=ReplyKeyboardMarkup(
                                    keyboard=job_categories_reply_keyboard, 
                                    one_time_keyboard=True,
                                    input_field_placeholder=input_field_placeholder,
                                    resize_keyboard=True))

    return CreateJob.CATEGORY_ID


async def validate_category_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_field_placeholder: str = 'Seleziona la categoria del lavoro dal menu sottostante:'

    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'La scelta inserita non e\' valida.\n' + \
                                    'Seleziona la categoria del lavoro:',
                                    reply_markup=ReplyKeyboardMarkup(
                                    keyboard=job_categories_reply_keyboard, 
                                    one_time_keyboard=True,
                                    input_field_placeholder=input_field_placeholder,
                                    resize_keyboard=True))
    
    return CreateJob.CATEGORY_ID


async def category_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the category_id (that here is string corresponding to the "name" column) of the job_category
    job_data['category_id'] = user_message
    
    # Ask for user input and remove the ReplyKeyboard
    await update.message.reply_text('Inserisci la posizione ricercata \U0001F477',
                                    reply_markup=ReplyKeyboardRemove())
    
    return CreateJob.POSITION


async def position(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the job's position
    job_data['position'] = user_message
    
    await update.message.reply_text('Inserisci una breve descrizione del lavoro \U0001F4C4')
    
    return CreateJob.DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the job's description
    job_data['description'] = user_message
    
    await update.message.reply_text(text='Inserisci il link dell\'offerta \U0001F310 \n' + \
                                         '<i>Se non applicabile: n.a.</i>', 
                                    parse_mode=ParseMode.HTML)
    
    return CreateJob.LINK


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the job's link
    job_data['link'] = user_message if user_message != 'n.a.' else None
    
    await update.message.reply_text(text='Inserisci il RAL del lavoro \U0001F4B2\n' + \
                                    '<i>Esempio: 50000</i>\n' + \
                                    '<i>Se non applicabile: n.a.</i>',
                                    parse_mode=ParseMode.HTML)
    
    return CreateJob.RAL


async def validate_ral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'La RAL inserita non e\' valida.\n' + \
                                    'Inserisci il RAL del lavoro:')
    
    return CreateJob.RAL


async def normalize_job(job_data: dict):

    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:

        # Get the respective contract_type_id by its name
        sql_statement: Select = select(ContractType.id).where(ContractType.name == job_data['contract_type_id'])
        contract_type_id: int = db_session.scalar(sql_statement)
        
        # Update the job_data dictionary
        job_data['contract_type_id'] = contract_type_id
        
        # Get the respective category_id by its name
        sql_statement: Select = select(JobCategory.id).where(JobCategory.name == job_data['category_id'])
        category_id: int = db_session.scalar(sql_statement)
        
        # Update the job_data dictionary
        job_data['category_id'] = category_id

        # Create the new job
        job: Job = Job(**job_data)

        # Add the job to the session
        db_session.add(job)
        
        # If the job has correctly added to the session
        if job in db_session:
            db_session.commit()
            return True
        
        return False


async def ral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text

    # Set the job's link and created_by (id of the user)
    job_data['ral'] = user_message if user_message != 'n.a.' else None
    job_data['created_by'] = update.message.from_user.id

    # Normalization of the data (contract_type_id and category_id strings (column "name") become ids)
    if await normalize_job(job_data):
        await update.message.reply_text('Lavoro creato correttamente \U00002705')
    
    # End of the conversation
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Operazione annullata dall\'utente \U0000274C', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


# Set the filter for the message handlers,
# in order to filter the messages and choose the correct callback
TEXT_FILTER_WITH_CANCEL_COMMAND = filters.TEXT & \
                                  ~filters.Regex(pattern=r'^\/cancel$')

# Create the job handler
create_job_handler: dict = {
    'entry_points': [
        CommandHandler(
            command='create_job', 
            callback=create_job
            )
    ],
    'states': {
        CreateJob.CONTRACT_TYPE: [
            MessageHandler(
                filters=filters.Regex(pattern=contract_types_filter_pattern), 
                callback=contract_type),
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=validate_contract_type)
                ],
        CreateJob.CATEGORY_ID: [
            MessageHandler(
                filters=filters.Regex(pattern=category_ids_filter_pattern), 
                callback=category_id),
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=validate_category_id)],
        CreateJob.POSITION: [
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=position)],
        CreateJob.DESCRIPTION: [
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=description)],
        CreateJob.LINK: [
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=link)],
        CreateJob.RAL: [
            MessageHandler(
                filters=(filters.Regex(r'^\d+$') | filters.Regex(r'^n\.a\.$')) & ~filters.Regex(pattern=r'^\/cancel$'), 
                callback=ral),
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND,
                callback=validate_ral)]
    },
    # Here is where the ConversationHandler goes when all the filters didn't pass the check
    'fallbacks': [CommandHandler('cancel', cancel)]
}