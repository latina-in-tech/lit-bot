from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


MESSAGE: str = '''
\U0001F4D6 <b>Regolamento del Gruppo:</b>
\U00002022 non e' ammesso alcun tipo di offesa diretta o indiretta verso un altro membro del gruppo \U0001F621
\U00002022 l'unico tipo di flame ammesso e' quello diretto alle tecnologie \U0001F525
\U00002022 utilizza i topics in maniera responsabile \U0001F37A
\U00002022 per segnalare un comportamento scorretto o qualcos'altro degno di nota dello staff, rispondi al messaggio da segnalare con il tag @admin \U0001F46E

Grazie e buona permanenza! \U0001F60A
'''


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(text=MESSAGE, parse_mode=ParseMode.HTML)
