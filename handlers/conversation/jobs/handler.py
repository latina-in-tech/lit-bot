from enum import Enum
from models.job.job import Job
from models.job.crud.retrieve import (retrieve_job_categories_with_jobs_count, retrieve_jobs, 
                                      retrieve_jobs_by_category, retrieve_job_category_pattern)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import (CallbackQueryHandler, CommandHandler, 
                          ContextTypes, ConversationHandler, 
                          MessageHandler, filters)
from telegram.constants import ParseMode
from re import findall
from utils.utils import close_inline_keyboard, create_inline_keyboard


HELP_MESSAGE: str = '''\U00002753 <b>Guida all'utilizzo del comando /jobs</b>
Visualizza la lista dei lavori proposti dai membri della community,
suddivisi per categoria.'''

class NavigateJobs(Enum):
    JOB_CATEGORY: int = 0
    GO_BACK: int = 1


async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    # Delete the user typed command
    await update.message.delete()
    
    # If there is any argument in the context
    if len(context.args) > 0:
    
        # If the first context argument is "help"
        if context.args[0] == 'help':
            await update.message.reply_text(text=HELP_MESSAGE, parse_mode=ParseMode.HTML)

            return

    # Variables initialization
    jobs_count: int = 0
    text: str = ''

    # Retrieving the list of job categories, with the count of jobs per category
    job_categories: list = await retrieve_job_categories_with_jobs_count()

    # Create the job categories inline keyboard
    job_categories_keyboard: InlineKeyboardMarkup = create_inline_keyboard(name='jck', 
                                                                           items=job_categories, 
                                                                           num_columns=2)
    
    # Get the jobs' list
    jobs_list: list[Job] = await retrieve_jobs()

    # If at least a job has been found
    if jobs_list:
                        
        # Get the records' count
        jobs_count = len(jobs_list)

        # Set the text to display to the user
        text = f'\U000025b6 Numero totale di lavori: {jobs_count}\n' + \
                'Clicca su una categoria per visualizzare la lista dei lavori.\n'
    
        # Send the message to the user
        await update.message.reply_text(text=text, 
                                        reply_markup=job_categories_keyboard,
                                        parse_mode=ParseMode.HTML)
        
        return NavigateJobs.JOB_CATEGORY
    
    else:
        await update.message.reply_text(text='Nessun lavoro trovato!')

        return ConversationHandler.END
    

async def handle_job_category(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # https://docs.python-telegram-bot.org/en/v20.8/telegram.callbackquery.html
    query: CallbackQuery = update.callback_query
    await query.answer()

    job_category_name = query.data
    text = f'Lista di lavori per la categoria "<i>{job_category_name}</i>":\n'

    # Get the list of jobs by category name
    jobs_list: list = await retrieve_jobs_by_category(job_category_name=job_category_name)
    
    # Compose the list of jobs
    for i, job in enumerate(jobs_list):
        text += f'{i + 1}. <a href="{job.link}">{job.position}</a>{f' - RAL: € {job.ral:,}' if job.ral else ''}\n'

    # Specify a callback_data is mandatory, otherwise the following error will be raised:
    # telegram.error.BadRequest: Can't parse inline keyboard button: text buttons are unallowed in the inline keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='\U000025C0 Indietro', callback_data='go_back')]
    ])
    
    await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    return NavigateJobs.GO_BACK


async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    await query.answer()
    
    # Variables initialization
    jobs_count: int = 0
    text: str = ''

    # Retrieving the list of job categories, with the count of jobs per category
    job_categories: list = await retrieve_job_categories_with_jobs_count()

    # Create the job categories inline keyboard
    job_categories_keyboard: InlineKeyboardMarkup = create_inline_keyboard(name='jck', 
                                                                           items=job_categories, 
                                                                           num_columns=2)
    
    # Get the jobs' list
    jobs_list: list[Job] = await retrieve_jobs()

    # If at least a job has been found
    if jobs_list:
                        
        # Get the records' count
        jobs_count = len(jobs_list)

        # Set the text to display to the user
        text = f'\U000025b6 Numero totale di lavori: {jobs_count}\n' + \
                'Clicca su una categoria per visualizzare la lista dei lavori.\n'
    
        # Send the message to the user
        await query.edit_message_text(text=text, 
                                        reply_markup=job_categories_keyboard,
                                        parse_mode=ParseMode.HTML)
        
        return NavigateJobs.JOB_CATEGORY
    
    else:
        await update.message.reply_text(text='Nessun lavoro trovato!')

        return ConversationHandler.END
    

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(text='Scelta non valida!')
    await update.message.delete()
    
    return
    

jobs_handler = {
    'entry_points': [
        CommandHandler(command='jobs', 
                       callback=jobs)
    ],
    'states': {
        NavigateJobs.JOB_CATEGORY: [
            CallbackQueryHandler(handle_job_category, pattern=retrieve_job_category_pattern()),         
        ],
        NavigateJobs.GO_BACK: [
            CallbackQueryHandler(go_back, pattern=r'^go_back$')
        ]
    },
    'fallbacks': [
        CallbackQueryHandler(close_inline_keyboard, pattern=r'^jck_close_inline_keyboard$'),
        MessageHandler(filters=filters.COMMAND | filters.TEXT, callback=handle_unknown)
    ]
}
