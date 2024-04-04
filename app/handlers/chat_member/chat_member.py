from datetime import datetime
from models.user.crud.update import update_user
from models.user.crud.retrieve import retrieve_user_by_telegram_id
from telegram import ChatMember, ChatMemberUpdated, Update
from telegram.ext import ContextTypes


async def extract_update_info(chat_member_update: ChatMemberUpdated) -> tuple | None:

    # Variables initialization
    is_member: bool = False
    was_member: bool = False

    # Get the difference of the update (if there is one)
    # The 'status' key is always present, and the value is None if the status didn't change,
    # otherwise the value is a tuple like (old_status, new_status)
    status: tuple = chat_member_update.difference().get('status')

    # If the status didn't change
    if not status:
        return None
    
    # Get the info about the status update
    old_status, new_status = status

    # Set the variables according to what the user did
    was_member = old_status == ChatMember.MEMBER and new_status == ChatMember.BANNED
    is_member = old_status == ChatMember.BANNED and new_status == ChatMember.MEMBER
    
    return was_member, is_member


async def on_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Extract the info about the updated chat member
    was_member, is_member = await extract_update_info(update.my_chat_member)

    # Get the Telegram user's id
    user_telegram_id: int = update.effective_user.id

    # If the member was a member and it's not a member (anymore),
    # it means that the user left the group, so flag it as deleted (soft-delete)
    if was_member and not is_member:
    
        # Obtain the user from its id
        if(user:=await retrieve_user_by_telegram_id(user_telegram_id)):
            
            # Update the deleted_at column
            user.deleted_at = datetime.now()
    
            # Update the user's info
            await update_user(user=user)
