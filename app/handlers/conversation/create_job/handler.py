from enum import Enum
from models.contract_type.crud.retrieve import (retrieve_contract_types, 
                                                retrieve_contract_type_id_by_name)
from models.job_category.crud.retrieve import (retrieve_job_categories, 
                                               retrieve_job_category_id_by_name)
from models.user.crud.retrieve import retrieve_user_by_telegram_id
from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import (ApplicationHandlerStop, 
                          ContextTypes, 
                          CommandHandler, 
                          ConversationHandler, 
                          filters, 
                          MessageHandler)
from utils.constants import ChatId, Emoji, ThreadId
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
    
    message: str = f'Ciao {update.effective_user.first_name}! {Emoji.WAVING_HAND}\n' + \
                   'Stai creando una nuova offerta di lavoro.\n' + \
                   'Digita il comando /cancel per annullare l\'operazione.\n\n' + \
                   f'Seleziona la tipologia di contratto {Emoji.MEMO}'
    
    await update.message.reply_text(text=message,
                                    reply_markup=contract_types_reply_keyboard)

    return CreateJob.CONTRACT_TYPE


async def validate_contract_type(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(f'Attenzione! {Emoji.WARNING}\n' + \
                                    'La scelta inserita non e\' valida.\n' + \
                                    'Seleziona la tipologia di contratto:',
                                    reply_markup=contract_types_reply_keyboard)
    
    return CreateJob.CONTRACT_TYPE


async def contract_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the contract_type_id (that here is string corresponding to the "name" column) of the contract_type
    job_data['contract_type_id'] = user_message

    await update.message.reply_text(f'Seleziona la categoria {Emoji.INPUT_LATIN_UPPERCASE}',
                                    reply_markup=job_categories_reply_keyboard)

    return CreateJob.CATEGORY_ID


async def validate_category_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(f'Attenzione! {Emoji.WARNING}\n' + \
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
    await update.message.reply_text(f'Inserisci la posizione ricercata {Emoji.CONSTRUCTION_WORKER}',
                                    reply_markup=ReplyKeyboardRemove())
    
    return CreateJob.POSITION


async def position(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the job's position
    job_data['position'] = user_message
    
    await update.message.reply_text(f'Inserisci una breve descrizione del lavoro {Emoji.PAGE_FACING_UP}')
    
    return CreateJob.DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the job's description
    job_data['description'] = user_message
    
    await update.message.reply_text(text=f'Inserisci il link dell\'offerta {Emoji.GLOBE_WITH_MERIDIANS}\n' + \
                                         '<i>Se non applicabile: n.a.</i>', 
                                    parse_mode=ParseMode.HTML)
    
    return CreateJob.LINK


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the job_data dictionary
    user_message: str = update.message.text
    
    # Set the job's link
    job_data['link'] = user_message if user_message != 'n.a.' else None
    
    await update.message.reply_text(text=f'Inserisci il compenso del lavoro (annuo o totale) {Emoji.EURO_BANKNOTE}\n' + \
                                    '<i>Esempio: 50000</i>\n' + \
                                    '<i>Se non applicabile: n.a.</i>',
                                    parse_mode=ParseMode.HTML)
    
    return CreateJob.RAL


async def validate_ral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(f'Attenzione! {Emoji.WARNING}\n' + \
                                    'Il compenso totale del lavoro non e\' corretto.\n' + \
                                    'Inserisci il compenso del lavoro (annuo o totale):')
    
    return CreateJob.RAL


async def normalize_job(job_data: dict):

    # Get the contract_type_id from its name
    contract_type_id: int = \
        await retrieve_contract_type_id_by_name(contract_type_name=job_data['contract_type_id'])
    
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
    job_data['created_by'] = retrieve_user_by_telegram_id(telegram_id=update.effective_user.id)

    # Normalization of the data (contract_type_id and category_id strings (column "name") become ids)
    if await normalize_job(job_data):
        
        # Create the job
        job = await models.job.crud.create.create_job(job_data=job_data)

        # If the job is correctly filled up
        if job:
            
            await update.message.reply_text(f'Lavoro creato correttamente {Emoji.CHECK_MARK_BUTTON}')

            # Compose the message to send to the group chat
            text: str = '\n'.join(f'<b>{k}</b>: {v}' for k,v in job.items())
            
            # Send the message to group chat
            # https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a
            await context.bot.send_message(chat_id=ChatId.GENERAL,
                                           message_thread_id=ThreadId.JOB,
                                           text=text,
                                           parse_mode=ParseMode.HTML)
    
    # End of the conversation
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(f'Operazione annullata dall\'utente {Emoji.CROSS_MARK}', 
                                    reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def unauthorized_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(f'I comandi non sono utilizzabili durante questo processo {Emoji.CROSS_MARK}')

    # Thanks to this raise, the update will not be processed
    # by other handlers, avoid calling other functions when
    # using the ConversationHandler
    raise ApplicationHandlerStop()


# Set the filter for the message handlers,
# in order to filter the messages and choose the correct callback
TEXT_FILTER = (filters.TEXT & 
               ~filters.COMMAND & 
               ~filters.Regex(pattern=r'^\/cancel$'))

CONTRACT_TYPE_FILTER = (filters.Regex(pattern=contract_types_filter_pattern) & 
                        ~filters.COMMAND)

CATEGORY_IDS_FILTER = (filters.Regex(pattern=category_ids_filter_pattern) & 
                       ~filters.COMMAND)

RAL_FILTER = ((filters.Regex(r'^\d+$') | filters.Regex(r'^n\.a\.$')) & 
              ~filters.COMMAND &
              ~filters.Regex(pattern=r'^\/cancel$'))
                        

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
                filters=CONTRACT_TYPE_FILTER,
                callback=contract_type),
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=validate_contract_type)
                ],
        CreateJob.CATEGORY_ID: [
            MessageHandler(
                filters=CATEGORY_IDS_FILTER, 
                callback=category_id),
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=validate_category_id)],
        CreateJob.POSITION: [
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=position)],
        CreateJob.DESCRIPTION: [
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=description)],
        CreateJob.LINK: [
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=link)],
        CreateJob.RAL: [
            MessageHandler(
                filters=RAL_FILTER, 
                callback=ral),
            MessageHandler(
                filters=TEXT_FILTER,
                callback=validate_ral)]
    },
    # Here is where the ConversationHandler goes when all the filters didn't pass the check
    # It's important to put the "unauthorized_commands" fallback after the "cancel" one,
    # otherwise the "cancel" command will never be invoked (because of filters=filters.COMMAND)
    # of the MessageHandler
    'fallbacks': [
        CommandHandler('cancel', cancel),
        MessageHandler(filters=filters.COMMAND, callback=unauthorized_commands)
        ]
}
