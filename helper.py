# Format user_data for first time start
from datetime import datetime


def format_user_data(update, context):
    user = update.message.from_user
    user_id = user['id']
    username = user['username']
    context.user_data["polls"] = {}
    context.user_data["poll count"] = 0
    context.user_data["Name"] = ""
    context.user_data["Username"] = username
    context.user_data["payment methods"] = {}
    post = {'_id': user_id, 'user_data': context.user_data}
    try:
        collection.insert_one(post)
    except:
        collection.find_one_and_replace({'_id': user_id}, {'_id': user_id, 'user_data': context.user_data})


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
