from datetime import datetime, time, timezone
from enum import Enum
from telegram import ReplyKeyboardRemove, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationHandlerStop, ContextTypes, CommandHandler, ConversationHandler, filters, MessageHandler
from models.event.crud.delete import soft_delete_event_by_id
from models.user.crud.retrieve import check_user_role
from utils.constants import ChatId, Emoji, ThreadId
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


# Initialize an empty dict for the new event's data
events_data: dict = {}


async def create_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the Telegram user
    user = update.effective_user
    
    # Check if the Telegram user has the specified role(s)
    if not await check_user_role(user_telegram_id=user.id, user_role='Administrator'):
        await update.message.reply_text(f'{Emoji.LOCKED} Non sei abilitato a compiere quest\'azione!')
        return
    
    message: str = f'Ciao {user.first_name}! {Emoji.WAVING_HAND}\n' + \
                   'Stai creando un nuovo evento.\n' + \
                   'Digita il comando /cancel per annullare l\'operazione.\n\n' + \
                   f'Inserisci il nome dell\'evento {Emoji.PENCIL}'
    
    await update.message.reply_text(text=message)

    return CreateEvent.NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['name'] = user_message

    await update.message.reply_text(f'Inserisci la descrizione dell\'evento {Emoji.MEMO}')

    return CreateEvent.DESCRIPTION


async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['description'] = user_message
    
    # Ask for user input and remove the ReplyKeyboard
    await update.message.reply_text(f'Inserisci la data dell\'evento {Emoji.CALENDAR}\n' + \
                                    '<i>Formato: DD/MM/YYYY</i>', 
                                    parse_mode=ParseMode.HTML)
    
    return CreateEvent.DATE


async def validate_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(f'Attenzione! {Emoji.WARNING}\n' + \
                                    'Il formato della data inserita non e\' corretto.\n' + \
                                    'Inserisci la data dell\'evento:')

    return CreateEvent.DATE
    

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['date'] = datetime.strptime(user_message, '%d/%m/%Y')
    
    await update.message.reply_text(f'Inserisci l\'ora di inizio dell\'evento {Emoji.ONE_O_CLOCK}')
    
    return CreateEvent.START_TIME


async def validate_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(f'Attenzione! {Emoji.WARNING}\n' + \
                                    'Il formato dell\'ora di inizio dell\'evento non e\' corretto.\n' + \
                                    'Inserisci l\'ora di inizio dell\'evento:')

    return CreateEvent.START_TIME


async def start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    events_data['start_time'] = user_message
    
    await update.message.reply_text(f'Inserisci l\'ora di fine dell\'evento {Emoji.EIGHT_O_CLOCK}')
    
    return CreateEvent.END_TIME


async def validate_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(f'Attenzione! {Emoji.WARNING}\n' + \
                                    'Il formato dell\'ora di fine dell\'evento non e\' corretto.' + \
                                    'Inserisci l\'ora di fine dell\'evento:')

    return CreateEvent.END_TIME


async def end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    # Set the event's end time
    events_data['end_time'] = user_message
    
    await update.message.reply_text(text=f'Inserisci la location dell\'evento {Emoji.ROUND_PUSHPIN}')
    
    return CreateEvent.LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the previous message in order to store its value in the event_data dictionary
    user_message: str = update.message.text
    
    # Set the event's location
    events_data['location'] = user_message
    
    await update.message.reply_text(text=f'Inserisci il link dell\'evento {Emoji.GLOBE_WITH_MERIDIANS}')
    
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

        # Obtaining the hours and minutes of the event,
        # converting them to int in order to use the time class
        if len(event_start_time_info := event.start_time.split(':')) > 1:
            hour, minute = [int(n) for n in event_start_time_info]
        else:
            hour = int(event_start_time_info[0])
            minute = 0

        # Creating the expiration date of the event
        # This value is converted to UTC timezone,
        # since the "when" parameter of the "run_once" function
        # accepts UTC datetime (if not specified something else)
        expiration_date: datetime = datetime.combine(date=event.date, 
                                                     time=time(hour=hour, minute=minute)
                                                    ).astimezone(timezone.utc)
        
        # Scheduling the job
        context.job_queue.run_once(callback=set_event_expiration,
                                   when=expiration_date, 
                                   data=event.id, 
                                   name=str(event.id))
        
        await update.message.reply_text(f'Evento creato correttamente {Emoji.CHECK_MARK_BUTTON}')

        event_info: dict = {
            'Nome': event.name,
            'Data': event.date,
            'Ora': f'{event.start_time} - {event.end_time}',
            'Location': event.location,
            'Link': event.link
        }

        # Compose the message to send to the group chat
        text: str = '\n'.join(f'<b>{k}</b>: {v}' for k,v in event_info.items())
        
        # Send the message to group chat
        # https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a
        await context.bot.send_message(chat_id=ChatId.GENERAL,
                                        message_thread_id=ThreadId.EVENT,
                                        text=text,
                                        parse_mode=ParseMode.HTML)

    # End of the conversation
    return ConversationHandler.END 


async def set_event_expiration(context: ContextTypes.DEFAULT_TYPE):
    
    # Get the event_id from the job data
    event_id = context.job.data
    
    # Soft-delete the event
    await soft_delete_event_by_id(event_id=event_id)


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
TEXT_FILTER = (filters.TEXT & \
               ~filters.COMMAND & \
               ~filters.Regex(pattern=r'^\/cancel$'))

DATE_FILTER = (filters.Regex(pattern=r'^\d{2}\/\d{2}\/\d{4}$') & \
               ~filters.Regex(r'^\/cancel$'))

HOUR_FILTER = (filters.Regex(r'^[0-1][0-9]|2[0-4](?::[0-5][0-9])?$') & \
               ~filters.Regex(r'^\/cancel$'))


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
                filters=TEXT_FILTER, 
                callback=name
                )
            ],
        CreateEvent.DESCRIPTION: [
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=description
                )
            ],
        CreateEvent.DATE: [
            MessageHandler(
                filters=DATE_FILTER,
                callback=date
            ),
            MessageHandler(
                filters=TEXT_FILTER,
                callback=validate_date
            )
        ],
        CreateEvent.START_TIME: [
            MessageHandler(
                filters=HOUR_FILTER, 
                callback=start_time
            ),
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=validate_start_time
            )
        ],
        CreateEvent.END_TIME: [
            MessageHandler(
                filters=HOUR_FILTER,
                callback=end_time
            ),
            MessageHandler(
                filters=TEXT_FILTER,
                callback=validate_end_time
            ),
        ],
        CreateEvent.LOCATION: [
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=location
            )
        ],
        CreateEvent.LINK: [
            MessageHandler(
                filters=TEXT_FILTER, 
                callback=link)]
    },
    # Here is where the ConversationHandler goes when all the filters didn't pass the check
    'fallbacks': [
        CommandHandler('cancel', cancel),
        MessageHandler(filters=filters.COMMAND, callback=unauthorized_commands)
    ]
}