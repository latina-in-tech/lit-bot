from datetime import datetime, timedelta, timezone
from captcha.image import ImageCaptcha
from random import choices, shuffle
from string import ascii_letters
from telegram import Update
from telegram.ext import ContextTypes
from utils.constants import Emoji
from utils.utils import create_inline_keyboard


async def chat_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get the user id of the user who is trying to join
    user_id: int = update.chat_join_request.from_user.id
    user_chat_id = update.chat_join_request.user_chat_id

    # Generate the job name for the captcha timer
    job_name: str = f'captcha_{user_id}'

    # Get the job from the job queue
    # This instruction is used for subsequent join requests
    captcha_job = jobs[0] if(jobs := context.job_queue.get_jobs_by_name(name=job_name)) else None

    # If the job exists, then it means that the user already did a chat join request,
    # and it needs to wait the timer to expire in order to make another one
    if captcha_job is None:
        
        # Set the run time of the job
        timer_expiration: datetime = (datetime.now() + timedelta(minutes=1)).astimezone(timezone.utc)
    
        # Job creation
        context.job_queue.run_once(callback=on_timer_expiration,
                                   when=timer_expiration,
                                   data=user_id,
                                   name=job_name)
    else:

        # Inform the user to wait the timer to expire
        await context.bot.send_message(chat_id=user_chat_id,
                                       text=f'{Emoji.ONE_O_CLOCK} Devi attendere tre minuti tra una richiesta di ingresso e l\'altra.')
        
        return

    # Generate the code and the image captcha
    image: ImageCaptcha = ImageCaptcha()
    correct_captcha_code: str = ''.join(choices(population=ascii_letters, k=4))
    data = image.generate(correct_captcha_code)

    # Save the user id and the correct captcha code in the bot_data dictionary
    context.bot_data[user_id] = f'{user_id}_{correct_captcha_code}'

    # Initialize a list of answers
    answers: list = []

    # Generate random answers
    for _ in range(3):
        
        # Convert the correct_captcha_code to a list of characters
        random_captcha_code_chars = list(correct_captcha_code)
        
        # Shuffle the characters
        shuffle(random_captcha_code_chars)
        
        # Join the shuffled list of characters
        random_captcha_code = ''.join(random_captcha_code_chars)

        # Append the answer to the list of answers (to create InlineKeyboardButtons)
        answers.append(
            {
                'text': random_captcha_code,
                'callback_data': f'captcha_{user_id}_{random_captcha_code}'
            }
        )

    # Append the correct answer
    answers.append(
        {
            'text': correct_captcha_code,
            'callback_data': f'captcha_{user_id}_{correct_captcha_code}'
        }
    )

    # Shuffle the list of answers
    shuffle(answers)

    # Create the captcha answers keyboard
    captcha_keyboard = create_inline_keyboard(name='captcha_inline_keyboard',
                                      items=answers,
                                      num_columns=2,
                                      has_close_button=False)

    # Send the captcha
    await context.bot.send_photo(chat_id=user_chat_id, 
                                 photo=data, 
                                 caption=f'{Emoji.LOCKED_WITH_KEY} Premi sul CAPTCHA corretto per proseguire:',
                                 reply_markup=captcha_keyboard)
        

async def chat_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get the callback query and answer it
    query = update.callback_query
    await query.answer()

    # Get the callback query data (which button the user pressed)
    callback_data = query.data

    # Split the data from bot_data dictionary
    # The split will produce three values (request)
    request_user_id, request_captcha = context.bot_data[update.effective_user.id].split('_')
    
    # Split the callback data
    # The split will produce three values (response)
    _, response_user_id, response_captcha = callback_data.split('_')

    # Generate the job name to get the captcha timer (if exists)
    job_name: str = f'captcha_{request_user_id}'
    
    # If the data from request is the same from the response, then approve the chat join request
    if request_user_id == response_user_id and request_captcha == response_captcha:
        
        await context.bot.approve_chat_join_request(chat_id=-1002052131071, user_id=request_user_id)
        
        # Schedule the removal of the job from the queue (if it exists)
        jobs[0].schedule_removal() if(jobs := context.job_queue.get_jobs_by_name(name=job_name)) else None

    else:
        # await context.bot.decline_chat_join_request(chat_id=-1002052131071, user_id=request_user_id)
        await update.effective_chat.send_message(f'{Emoji.CROSS_MARK} Captcha fallito!')
        
    # Delete the captcha in any case
    await query.delete_message()

    # Clear the bot_data dictionary
    context.bot_data.clear()


async def on_timer_expiration(context: ContextTypes.DEFAULT_TYPE):

    # Get the job that triggered the callback
    job = context.job

    # Get the user id of the user who made the request to join
    user_id: int = job.data

    # Inform the user that it can do another chat join request
    await context.bot.send_message(chat_id=user_id, 
                                   text=f'{Emoji.GREEN_CIRCLE} Puoi effettuare una nuova richiesta di accesso al gruppo.')