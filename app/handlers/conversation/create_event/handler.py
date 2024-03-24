from datetime import datetime
from enum import Enum
from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, filters, MessageHandler
from models.user.crud.retrieve import user_is_administrator
import models.event.crud.create


# CreateEvent Enum for the ConversationHandler steps
class CreateEvent(Enum):
    NAME: int = 0 
    DESCRIPTION: int = 1
    DATE: int = 2
    START_TIME: int = 3
    END_TIME: int = 4
    LOCATION: int = 5
    LINK: int = 6


EVENTS_GROUP_CHAT_ID: int = -1001847839591
EVENTS_GROUP_THREAD_ID: int = 24

# Initialize an empty dict for the new event's data
events_data: dict = {}  


async def create_event(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    
    if not await user_is_administrator(update.effective_user.id):
        await update.message.reply_text('\U0001F512 Non sei abilitato a compiere quest\'azione!')
        return 
    
    message: str = f'Ciao {update.effective_user.first_name}! \U0001F44B\n' + \
                   'Stai creando un nuovo evento.\n' + \
                   'Digita il comando /cancel per annullare l\'operazione.\n\n' + \
                   'Inserisci il nome dell\'evento \U0000270F' 
    
    await update.message.reply_text(text=message)

    return CreateEvent.NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['name'] = user_message

    await update.message.reply_text('Inserisci la descrizione dell\'evento \U0001F4DD')

    return CreateEvent.DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['description'] = user_message
    
    # Ask for user input and remove the ReplyKeyboard
    await update.message.reply_text('Inserisci la data dell\'evento \U0001F4C5\n' + \
                                    '<i>Formato: DD/MM/YYYY</i>', 
                                    parse_mode=ParseMode.HTML)
    
    return CreateEvent.DATE


async def validate_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'Il formato della data inserita non e\' corretto.\n' + \
                                    'Inserisci la data dell\'evento:')

    return CreateEvent.DATE
    

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['date'] = datetime.strptime(user_message, '%d/%m/%Y')
    
    await update.message.reply_text('Inserisci l\'ora di inizio dell\'evento \U0001F550')
    
    return CreateEvent.START_TIME


async def validate_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'Il formato dell\'ora di inizio dell\'evento non e\' corretto.\n' + \
                                    'Inserisci l\'ora di inizio dell\'evento:')

    return CreateEvent.START_TIME


async def start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['start_time'] = user_message
    
    await update.message.reply_text('Inserisci l\'ora di fine dell\'evento \U0001F557')
    
    return CreateEvent.END_TIME


async def validate_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text('Attenzione! \U000026A0\n' + \
                                    'Il formato dell\'ora di fine dell\'evento non e\' corretto.' + \
                                    'Inserisci l\'ora di fine dell\'evento:')

    return CreateEvent.END_TIME


async def end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    # Set the event's end time
    events_data['end_time'] = user_message
    
    await update.message.reply_text(text='Inserisci la location dell\'evento \U0001F4CD')
    
    return CreateEvent.LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    # Set the event's location
    events_data['location'] = user_message
    
    await update.message.reply_text(text='Inserisci il link dell\'evento \U0001F310')
    
    return CreateEvent.LINK


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text

    # Set the event's link and created_by (id of the user)
    events_data['link'] = user_message
    events_data['created_by'] = update.message.from_user.id
    
    # Create the event
    event = await models.event.crud.create.create_event(event_data=events_data)

    # If the event is correctly filled up
    if event:
        
        await update.message.reply_text('Evento creato correttamente \U00002705')

        # Compose the message to send to the group chat
        text: str = '\n'.join(f'<b>{k}</b>: {v}' for k,v in event.items())
        
        # Send the message to group chat
        # https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a
        await context.bot.send_message(chat_id=EVENTS_GROUP_CHAT_ID,
                                        message_thread_id=EVENTS_GROUP_THREAD_ID,
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

# Create the event handler
create_event_handler: dict = {
    'entry_points': [
        CommandHandler(
            command='create_event', 
            callback=create_event,
            filters=filters.ChatType.PRIVATE
            )
    ],
    'states': {
        CreateEvent.NAME: [
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=name
                )
            ],
        CreateEvent.DESCRIPTION: [
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=description
                )
            ],
        CreateEvent.DATE: [
            MessageHandler(
                filters=filters.Regex(pattern=r'\d{2}\/\d{2}\/\d{4}') & ~filters.Regex(r'^\/cancel'),
                callback=date
            ),
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND,
                callback=validate_date
            )
        ],
        CreateEvent.START_TIME: [
            MessageHandler(
                filters=filters.Regex(pattern=r'^\d+(?::\d+)?$') & ~filters.Regex(r'\/cancel'), 
                callback=start_time
            ),
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=validate_start_time
            )
        ],
        CreateEvent.END_TIME: [
            MessageHandler(
                filters=filters.Regex(pattern=r'^\d+(?::\d+)?$') & ~filters.Regex(r'\/cancel'),
                callback=end_time
            ),
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND,
                callback=validate_end_time
            ),
        ],
        CreateEvent.LOCATION: [
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=location
            )
        ],
        CreateEvent.LINK: [
            MessageHandler(
                filters=TEXT_FILTER_WITH_CANCEL_COMMAND, 
                callback=link)]
    },
    # Here is where the ConversationHandler goes when all the filters didn't pass the check
    'fallbacks': [CommandHandler('cancel', cancel)]
}