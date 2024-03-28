from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


# Chat ID of the group chat (General topic)
GENERAL_CHAT_ID: int = -1001847839591

COMMANDS_LIST: list = [
    {
        'name': '/cmds', 
        'description': 'Visualizza la lista dei comandi eseguibili dal bot', 
        'requires_admin': False
    },
    {
        'name': '/contacts', 
        'description': 'Visualizza i contatti della LiT', 
        'requires_admin': False
    },
    {
        'name': '/create_job', 
        'description': 'Crea una nuova offerta di lavoro', 
        'requires_admin': False
    },
    {
        'name': '/events', 
        'description': 'Visualizza la lista degli eventi della community in programma', 
        'requires_admin': False
    },
    {
        'name': '/faq', 
        'description': 'Visualizza le FAQ del gruppo', 
        'requires_admin': False
    },
    {
        'name': '/get_user_role', 
        'description': 'Ottiene il ruolo dell\'utente specificato', 
        'requires_admin': True
    },
    {
        'name': '/jobs', 
        'description': 'Visualizza la lista dei lavori proposti dai membri della community', 
        'requires_admin': False
    },
    {
        'name': '/rules', 
        'description': 'Visualizza le regole del gruppo', 
        'requires_admin': False
    },
    {
        'name': '/set_user_role', 
        'description': 'Imposta il ruolo dell\'utente specificato', 
        'requires_admin': False
    },
    {
        'name': '/slides', 
        'description': 'Visualizza il link per scaricare i template delle slides per i talk della LiT', 
        'requires_admin': False
    },
    {
        'name': '/start', 
        'description': 'Avvia il bot', 
        'requires_admin': False
    }
]

async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_commands: list = []
    admin_commands: list = []
    
    chat_member = await context.bot.get_chat_member(chat_id=GENERAL_CHAT_ID, 
                                                    user_id=update.effective_user.id)

    # Compose the text to show to the user
    for command in COMMANDS_LIST:
        if not command['requires_admin']:
            user_commands.append(command)
        
        admin_commands.append(command)
    
    if chat_member.status == ChatMember.ADMINISTRATOR:
        message: str = '\U0001F4BB <b>Lista dei comandi disponibili:</b>\n'
    
        for command in admin_commands:
            message += f'{command['name']} - {command['description']}\n'
    
    else:
        
        for command in user_commands:
            message += f'{command['name']} - {command['description']}\n'

    await update.message.reply_text(text=message, parse_mode=ParseMode.HTML)
