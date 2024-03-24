from enum import Enum
from models.contract_type.crud.retrieve import retrieve_contract_types, retrieve_contract_type_id_by_name
from models.job_category.crud.retrieve import retrieve_job_categories, retrieve_job_category_id_by_name
from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, filters, MessageHandler
from utils.utils import create_reply_keyboard
import models.job.crud.create


# CreateJob Enum for the ConversationHandler steps
class CreateJob(Enum):
    CONTRACT_TYPE: int = 0 
    CATEGORY_ID: int = 1
    POSITION: int = 2
    DESCRIPTION: int = 3
    LINK: int = 4
    RAL: int = 5

# The actual group_chat_id is 1847839591, but in order to use it with the APIs,
# we need to add the prefix of -100
# https://t.me/c/1847839591/23/10957
JOB_OFFERS_GROUP_CHAT_ID: int = -1001847839591
JOB_OFFERS_GROUP_THREAD_ID: int = 23

# Initialize an empty dict for the new job's data
job_data: dict = {}

# Get list of contract types
contract_types = retrieve_contract_types()

# Set the text to be displayed as hint in the text input field
input_field_placeholder: str = 'Seleziona la tipologia di contratto del lavoro dal menu sottostante:'    

# Keyboard
# Each row is a list, and each button is an item
contract_types_reply_keyboard: list = create_reply_keyboard(items=contract_types, 
                                                            num_columns=3,
                                                            input_field_placeholder=input_field_placeholder,
                                                            has_close_button=False)
        
# Filter pattern
contract_types_filter_pattern: str = f'^({'|'.join(contract_types)})$'

# Get list of job cateegories
job_categories: list = retrieve_job_categories()

# Keyboard
# Each row is a list, and each button is an item
job_categories_reply_keyboard = create_reply_keyboard(items=job_categories, 
                                                            num_columns=2,
                                                            input_field_placeholder=input_field_placeholder,
                                                            has_close_button=False)
        
# Filter pattern
category_ids_filter_pattern = f'^({'|'.join(job_categories)})$'


async def create_job(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    
    message: str = f'Ciao {update.effective_user.first_name}! \U0001F44B\n' + \
                   'Stai creando una nuova offerta di lavoro.\n' + \
                   'Digita il comando /cancel per annullare l\'operazione.\n\n' + \
                   'Seleziona la tipologia di contratto \U0001F4DD'
    
    await update.message.reply_text(text=message,
                                    reply_markup=contract_types_reply_keyboard)

    return CreateJob.CONTRACT_TYPE


async def validate_contract_type(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'La scelta inserita non e\' valida.\n' + \
                                    'Seleziona la tipologia di contratto:',
                                    reply_markup=contract_types_reply_keyboard)
    
    return CreateJob.CONTRACT_TYPE


async def contract_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the contract_type_id (that here is string corresponding to the "name" column) of the contract_type
    job_data['contract_type_id'] = user_message

    await update.message.reply_text('Seleziona la categoria \U0001F520',
                                    reply_markup=job_categories_reply_keyboard)

    return CreateJob.CATEGORY_ID


async def validate_category_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'La scelta inserita non e\' valida.\n' + \
                                    'Seleziona la categoria del lavoro:',
                                    reply_markup=job_categories_reply_keyboard)
    
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
    
    await update.message.reply_text(text='Inserisci il compenso del lavoro (annuo o totale) \U0001F4B2\n' + \
                                    '<i>Esempio: 50000</i>\n' + \
                                    '<i>Se non applicabile: n.a.</i>',
                                    parse_mode=ParseMode.HTML)
    
    return CreateJob.RAL


async def validate_ral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'Il compenso totale del lavoro non e\' corretto.\n' + \
                                    'Inserisci il compenso del lavoro (annuo o totale):')
    
    return CreateJob.RAL


async def normalize_job(job_data: dict):

    # Get the contract_type_id from its name
    contract_type_id: int = await retrieve_contract_type_id_by_name(contract_name=job_data['contract_type_id'])
    
    # Update the job_data dictionary
    job_data['contract_type_id'] = contract_type_id
    
    # Get the job_category_id from its name
    category_id: int = await retrieve_job_category_id_by_name(job_category_name=job_data['category_id'])
    
    # Update the job_data dictionary
    job_data['category_id'] = category_id

    return True


async def ral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text

    # Set the job's link and created_by (id of the user)
    job_data['ral'] = user_message if user_message != 'n.a.' else None
    job_data['created_by'] = update.message.from_user.id

    # Normalization of the data (contract_type_id and category_id strings (column "name") become ids)
    if await normalize_job(job_data):
        
        # Create the job
        job = await models.job.crud.create.create_job(job_data=job_data)

        # If the job is correctly filled up
        if job:
            
            await update.message.reply_text('Lavoro creato correttamente \U00002705')

            # Compose the message to send to the group chat
            text: str = '\n'.join(f'<b>{k}</b>: {v}' for k,v in job.items())
            
            # Send the message to group chat
            # https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a
            await context.bot.send_message(chat_id=JOB_OFFERS_GROUP_CHAT_ID,
                                           message_thread_id=JOB_OFFERS_GROUP_THREAD_ID,
                                           text=text,
                                           parse_mode=ParseMode.HTML)
    
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
            callback=create_job,
            filters=filters.ChatType.PRIVATE
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