# Format user_data for first time start
from datetime import datetime


def get_user_id(update, context):
    user = update.message.from_user
    user_id = user['id']
    return str(user_id)


def get_chat_id(update, context):
    chat_id = update.effective_chat.id
    return str(chat_id)


def get_today_midnight():
    now = datetime.now().date()
    return datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )
