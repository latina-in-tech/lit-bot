from enum import Enum
from models.job.crud.retrieve import retrieve_job_categories_with_jobs_count, retrieve_jobs
from models.job.job import Job
from telegram import InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from typing import classmethod
from utils.utils import create_inline_keyboard


HELP_MESSAGE: str = '''\U00002753 <b>Guida all'utilizzo del comando /jobs</b>
Visualizza la lista dei lavori proposti dai membri della community,
suddivisi per categoria.'''

class NavigateJobs(Enum):
    JOB_CATEGORY: int = 0
    GO_BACK: int = 1


class JobConversationHandler():

    # Message to display to the user
    message: str = ''
    
    @classmethod
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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

        # Retrieving the list of job categories, with the count of jobs per category
        job_categories: list = await retrieve_job_categories_with_jobs_count()

        # Create the job categories inline keyboard
        job_categories_keyboard: InlineKeyboardMarkup = create_inline_keyboard(items=job_categories, num_columns=2)
        
        # Get the jobs' list
        jobs_list: list[Job] = await retrieve_jobs()

        # If at least a job has been found
        if jobs_list:
                            
            # Get the records' count
            jobs_count = len(jobs_list)

            # Set the text to display to the user
            self.message = (f'\U000025b6 Numero totale di lavori: {jobs_count}\n'
                            'Clicca su una categoria per visualizzare la lista dei lavori.\n')
        
            # Send the message to the user
            await update.message.reply_text(text=self.message, 
                                            reply_markup=job_categories_keyboard,
                                            parse_mode=ParseMode.HTML)
            
            return NavigateJobs.JOB_CATEGORY
        
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Nessun lavoro trovato!')

            return ConversationHandler.END
        
