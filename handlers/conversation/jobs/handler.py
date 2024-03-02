from dependencies.db import SessionLocal
from models.job.job import Job
from sqlalchemy import Result, ScalarResult, Select, select
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram.constants import ParseMode
from re import findall
from sqlalchemy import func
from models.job_category.job_category import JobCategory
from itertools import batched


HELP_MESSAGE: str = '''\U00002753 <b>Guida all'utilizzo del comando /jobs</b>
Visualizza la lista dei lavori proposti dai membri della community,
suddivisi per categoria.'''

JOB_CATEGORY, GO_BACK = range(2)
JOB_CATEGORY_PATTERN: str = r'(.*)\s\(\d+\)'


def create_inline_keyboard(num_columns: int, items: list) -> InlineKeyboardMarkup:
        
    keyboard: list = [
        [InlineKeyboardButton(text=item, callback_data=item) for item in list(batch)] 
        for batch in batched(iterable=items, n=num_columns)]
    
    keyboard.append(
        [
            InlineKeyboardButton(text='Chiudi \U0000274C', 
                                 callback_data='close_inline_keyboard')
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_job_categories_inline_keyboard():

    job_categories: list = []
    job_category_name: str = ''
    job_category_count: int = 0

    with SessionLocal() as db_session:

        # Obtain the count and the name for each job category
        sql_statement: Select = select(func.count(Job.id), JobCategory.name) \
                                .join(JobCategory, Job.job_category) \
                                .where(Job.deleted_at.is_(None)) \
                                .group_by(Job.category_id)
        
        # Executing the SELECT statement
        query_result: Result = db_session.execute(sql_statement)

        if query_result:
            
            # Compose the list for the keyboard
            for record in query_result:
                job_category_count, job_category_name = record
                job_categories.append(f'{job_category_name} ({job_category_count})')

            job_categories_keyboard = create_inline_keyboard(num_columns=2, items=job_categories)

        return job_categories_keyboard


async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    job_categories_keyboard = get_job_categories_inline_keyboard()
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Select statement for the jobs' list
        select_statement: Select = select(Job) \
                                  .where(Job.deleted_at.is_(None)) \
                                  .order_by(Job.created_at.desc())
        
        # Execute the query and get the result
        query_result: ScalarResult = db_session.scalars(select_statement).all()

        # If the query returned some data
        if query_result:
            
            # Get the records' count
            jobs_count = len(query_result)

            # Set the text to display to the user
            text = f'\U000025b6 Numero totale di lavori: {jobs_count}\n' + \
                   'Clicca su una categoria per visualizzare la lista dei lavori.\n'
        
            # Send the message to the user
            await update.message.reply_text(text=text, 
                                            reply_markup=job_categories_keyboard,
                                            parse_mode=ParseMode.HTML)
            
            return JOB_CATEGORY
        
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Nessun lavoro trovato!')

        return ConversationHandler.END
    

async def handle_job_category(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # https://docs.python-telegram-bot.org/en/v20.8/telegram.callbackquery.html
    query: CallbackQuery = update.callback_query
    await query.answer()

    callback_data = query.data
    job_category_name: str = findall(pattern=JOB_CATEGORY_PATTERN, string=callback_data)[0]
    text = f'Lista di lavori per la categoria "<i>{job_category_name}</i>":\n'

    with SessionLocal() as db_session:
    
        sql_statement: Select = select(JobCategory.id) \
                                .where(JobCategory.name == job_category_name)
        
        job_category_id = db_session.scalar(sql_statement)

        sql_statement: Select = select(Job) \
                                .where(Job.category_id == job_category_id)
        
        jobs = db_session.scalars(sql_statement).all()

        # Compose the list of jobs
        for i, job in enumerate(jobs):
            text += f'{i + 1}. <a href="{job.link}">{job.position}</a> - Dettagli\n'

        # Specify a callback_data is mandatory, otherwise the following error will be raised:
        # telegram.error.BadRequest: Can't parse inline keyboard button: text buttons are unallowed in the inline keyboard
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='\U000025C0 Indietro', callback_data='go_back')]
        ])
        
        await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

        return GO_BACK
    

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    query.answer()
    
    # Variables initialization
    jobs_count: int = 0
    text: str = ''

    job_categories_keyboard = get_job_categories_inline_keyboard()
    
    # Initialize the db_session
    # It closes automatically at the end of the "with" context manager
    with SessionLocal() as db_session:
    
        # Select statement for the jobs' list
        select_statement: Select = select(Job) \
                                  .where(Job.deleted_at.is_(None)) \
                                  .order_by(Job.created_at.desc())
        
        # Execute the query and get the result
        query_result: ScalarResult = db_session.scalars(select_statement).all()

        # If the query returned some data
        if query_result:
            
            # Get the records' count
            jobs_count = len(query_result)

            # Set the text to display to the user
            text = f'\U000025b6 Numero totale di lavori: {jobs_count}\n' + \
                   'Clicca su una categoria per filtrare la lista dei lavori.\n'
        
            # Send the message to the user
            await query.edit_message_text(text=text, 
                                          reply_markup=job_categories_keyboard,
                                          parse_mode=ParseMode.HTML)
            
            return JOB_CATEGORY
        
        else:
            await query.edit_message_text(text='Nessun lavoro trovato!')

        return ConversationHandler.END
    

async def close_inline_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query: CallbackQuery = update.callback_query
    query.answer()

    await query.delete_message()

    return ConversationHandler.END


async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    keyboard = InlineKeyboardMarkup([[]])

    await update.message.reply_text(text='Scelta non valida!', reply_markup=keyboard)

    update.message.delete()
    
    return ConversationHandler.END


jobs_handler = {
    'entry_points': [
        CommandHandler(command='jobs', 
                       callback=jobs)
    ],
    'states': {
        JOB_CATEGORY: [
            CallbackQueryHandler(handle_job_category, pattern=JOB_CATEGORY_PATTERN)
        ],
        GO_BACK: [
            CallbackQueryHandler(go_back, pattern='^go_back$')
        ]
    },
    'fallbacks': [
        CallbackQueryHandler(close_inline_keyboard, pattern='^close_inline_keyboard$'),
        MessageHandler(filters=filters.COMMAND | filters.TEXT, callback=handle_unknown),
        ]
}