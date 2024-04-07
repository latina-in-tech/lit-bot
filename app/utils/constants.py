from enum import IntEnum, StrEnum


# Bot Commands
BOT_COMMANDS: list[dict] = [
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
        'name': '/create_event', 
        'description': 'Crea un nuovo evento', 
        'requires_admin': True
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
        'requires_admin': True
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

# Character Enum
class Character(StrEnum):
    CIRCLE: str = '\U00002022'


# Emoji Enum
class Emoji(StrEnum):
    ATOM_SYMBOL: str = '\U0000269B'
    BEER_MUG: str = '\U0001F37A'
    BOOKS: str = '\U0001F4DA'
    CALENDAR: str = '\U0001F4C5'
    CHECK_MARK_BUTTON: str = '\U00002705'
    CLOUD: str = '\U00002601'
    CONSTRUCTION_WORKER: str = '\U0001F477'
    CROSS_MARK: str = '\U0000274C'
    EIGHT_O_CLOCK: str = '\U0001F557'
    ENRAGED_FACE: str = '\U0001F621'
    EURO_BANKNOTE: str = '\U0001F4B6'
    FACE_WITH_TEARS_OF_JOY: str = '\U0001F602'
    FIRE: str = '\U0001F525'
    GLOBE_WITH_MERIDIANS: str = '\U0001F310'
    GRINNING_FACE_WITH_SMILING_EYES: str = '\U0001F604'
    INPUT_LATIN_UPPERCASE: str = '\U0001F520'
    LOCKED: str = '\U0001F512'
    LOCKED_WITH_KEY: str = '\U0001F510'
    MEMO: str = '\U0001F4DD'
    MOBILE_PHONE: str = '\U0001F4F1'
    ONE_O_CLOCK: str = '\U0001F550'
    OPEN_BOOK: str = '\U0001F4D6'
    PAGE_FACING_UP: str = '\U0001F4C4'
    PERSON_SHRUGGING: str = '\U0001F937'
    PLAY_BUTTON: str = '\U000025B6'
    POLICE_OFFICER: str = '\U0001F46E'
    PENCIL: str = '\U0000270F'
    RED_QUESTION_MARK: str = '\U00002753'
    REVERSE_BUTTON: str = '\U000025C0'
    ROBOT: str = '\U0001F916'
    ROUND_PUSHPIN: str = '\U0001F4CD'
    SMILING_FACE_WITH_SMILING_EYES: str = '\U0001F60A'
    TECHNOLOGIST: str = '\U0001F4BB'
    UP_RIGHT_ARROW: str = '\U00002197'
    WARNING: str = '\U000026A0'
    WAVING_HAND: str = '\U0001F44B'


# ChatId Enum
class ChatId(IntEnum):
    GENERAL: int = -1001847839591


# ThreadId Enum
class ThreadId(IntEnum):
    GENERAL: int = 1
    JOB: int = 23
    EVENT: int = 24


