from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.constants import Emoji, Character


MESSAGE: str = f'''{Emoji.RED_QUESTION_MARK} <b>FAQ:</b>
<i>Che cos'è Latina in Tech (LiT)?</i>
Si tratta di una comunita' (lo so, fa tanto centro di recupero per tossicodipendenti {Emoji.GRINNING_FACE_WITH_SMILING_EYES}), 
il cui fulcro e' un gruppo Telegram suddiviso in topics, con l'obiettivo di mettere in contatto appassionati
del mondo tech nel contesto geografico di Latina e dintorni.

<i>Qual è il suo obiettivo?</i>
{Character.CIRCLE} Favorire la condivisione di conoscenza e la crescita professionale nel settore IT;
{Character.CIRCLE} Entrare in contatto (sia telematicamente che tramite eventi in presenza) con persone con interessi in comune nell'ambito della tecnologia e affini;

<i>Ma quindi, cosa ci si guadagna?</i>
Niente... o <b>tutto</b>!
LiT e' una possibilita' interessante di <b>arricchire il proprio background</b> tramite il racconto delle esperienze (anche tecniche) altrui, 
grazie al grande bacino di persone dal quale attingere per trovare <b>collaboratori</b> e per <b>dare visibilita' alle proprie idee</b> di progetto,
anche solamente per un consiglio di approccio ad una determinata problematica.

<b>TL;DR</b>: conoscere persone con cui sedersi davanti a una birra (pardon, Coca-Cola per gli astemi {Emoji.FACE_WITH_TEARS_OF_JOY}).
'''

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(text=MESSAGE, parse_mode=ParseMode.HTML)
