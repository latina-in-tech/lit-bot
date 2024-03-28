from handlers.command.cmds import COMMANDS_LIST
from telegram import ChatMember, Update, BotCommand, MenuButton, MenuButtonCommands
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from models.user.crud.create import save_user_info


# Chat ID of the group chat (General topic)
GENERAL_CHAT_ID: int = -1001847839591


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_commands: list = []
    admin_commands: list = []
    bot_commands: list[BotCommand] = []

    # Get the user who sent the /start command
    user = update.effective_user
    
    # Update the start message
    message: str = f'Ciao {user.full_name}! \U0001F44B\n' + \
                    'Sono il bot del gruppo Latina In Tech \U0001F916\n' + \
                    'Utilizza il comando /cmds per visualizzare la lista dei comandi disponibili.'


    # Send start message
    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
    
    chat_member = await context.bot.get_chat_member(chat_id=GENERAL_CHAT_ID, 
                                                    user_id=update.effective_user.id)

    # Compose the text to show to the user
    for command in COMMANDS_LIST:
        if not command['requires_admin']:
            user_commands.append(command)
        
        admin_commands.append(command)

    # Compose the text to show to the user
    for command in COMMANDS_LIST:
        if not command['requires_admin']:
            user_commands.append(command)
        
        admin_commands.append(command)

    if chat_member.status == ChatMember.ADMINISTRATOR:

        for command in admin_commands:
            bot_command = BotCommand(command=command['name'], 
                                     description=command['description'])
            
            bot_commands.append(bot_command)

    else:
        for command in user_commands:
            bot_command = BotCommand(command=command['name'], 
                                     description=command['description'])
            
            bot_commands.append(bot_command)

    # Set list of commands to the bot
    await context.bot.set_my_commands(commands=bot_commands)

    # Set menu button to show available bot commands
    await update.effective_chat.set_menu_button(menu_button=MenuButton(type=MenuButtonCommands.COMMANDS))

    # Save user's info
    await save_user_info(telegram_user=user)