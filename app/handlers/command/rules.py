from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import Character, Emoji


MESSAGE: str = f'''
{Emoji.OPEN_BOOK} <b>Regolamento del Gruppo:</b>
{Character.CIRCLE} non e' ammesso alcun tipo di offesa diretta o indiretta verso un altro membro del gruppo {Emoji.ENRAGED_FACE}
{Character.CIRCLE} l'unico tipo di flame ammesso e' quello diretto alle tecnologie {Emoji.FIRE}
{Character.CIRCLE} utilizza i topics in maniera responsabile {Emoji.BEER_MUG}
{Character.CIRCLE} per segnalare un comportamento scorretto o qualcos'altro degno di nota dello staff, rispondi al messaggio da segnalare con il tag @admin {Emoji.POLICE_OFFICER}

Grazie e buona permanenza! {Emoji.SMILING_FACE_WITH_SMILING_EYES}
'''


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(text=MESSAGE, parse_mode=ParseMode.HTML)
