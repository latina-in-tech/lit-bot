from handlers.command.cmds import COMMANDS_LIST
from telegram import Update, BotCommand, MenuButton, MenuButtonCommands
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from models.user.crud.create import save_user_info


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

    # Get the user who sent the /start command
    user = update.effective_user
    
    # Update the start message
    message: str = f'Ciao {user.full_name}! \U0001F44B\n' + \
                    'Sono il bot del gruppo Latina In Tech \U0001F916\n' + \
                    'Utilizza il comando /cmds per visualizzare la lista dei comandi disponibili.'


    # Send start message
    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)

    # Get the list of available commands from UDF commands
    bot_commands: list[BotCommand] = [BotCommand(command_name, command_description) 
                                      for command_name, command_description in COMMANDS_LIST.items()]

    # Set list of commands to the bot
    await context.bot.set_my_commands(commands=bot_commands)

    # Set menu button to show available bot commands
    await update.effective_chat.set_menu_button(menu_button=MenuButton(type=MenuButtonCommands.COMMANDS))

    # Save user's info
    await save_user_info(telegram_user=user)