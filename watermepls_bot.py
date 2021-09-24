from datetime import datetime, time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, InlineQueryHandler, \
    CallbackQueryHandler, DictPersistence
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import logging
import os

from helper import get_user_id, get_chat_id, get_today_midnight
from plant import Plant
from watermepls_mongo import add_new_user, add_new_plant, add_new_timing, get_all_ids, get_all_plant_name_with_id

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ['TOKEN']

# For logging purposes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# First time starting the bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to WaterMePlsBot [Beta Test Version]! U+2728",
                             parse_mode='HTML')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Before we begin, let me get to know you!\n\nWhat is your name?")
    return USERNAME


def create_user(update, context):
    uid = get_user_id(update, context)
    chat_id = get_chat_id(update, context)
    name = update.message.text

    add_new_user(uid, name, chat_id)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Thanks {} for joining the WaterMePls community!\n\nlet's start by adding your "
                                  "plants!".format(name))
    return ConversationHandler.END


def cancel(update, context):
    return ConversationHandler.END


# First Time Login Conversation
USERNAME = range(1)

registration_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        USERNAME: [
            MessageHandler(
                Filters.text & (~Filters.command), create_user
            )
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    conversation_timeout=300
)

# Adding a plant
new_plant = Plant()


def add_plant(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Time to add a plant! \nFirstly, what type of plant is this? (Eg. Sunflower, "
                                  "Cactus, etc.)",
                             parse_mode='HTML')
    plant_type = update.message.text
    new_plant.set_type(plant_type)
    return ADDPLANT


def ask_for_plant_name(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="What is your name for this plant? (Research has shown that naming your plant makes "
                                  "it healthier!)",
                             parse_mode='HTML')
    plant_name = update.message.text
    new_plant.set_name(plant_name)
    return REGISTERPLANT


def register_plant(update, context):
    uid = get_user_id(update, context)
    add_new_plant(uid, new_plant)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="We welcome {} to the family! Let's work together to take good care of it!".format(new_plant.name),
                             parse_mode='HTML')
    return ConversationHandler.END


# Adding a plant Conversation
ADDPLANT,REGISTERPLANT = range(2)

add_plant_handler = ConversationHandler(
    entry_points=[CommandHandler('add_plant', add_plant)],
    states={
        ADDPLANT: [
            MessageHandler(
                Filters.text & (~Filters.command), ask_for_plant_name
            ),
        ],
        REGISTERPLANT: [
            MessageHandler(
                Filters.text & (~Filters.command), register_plant
            ),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    conversation_timeout=300
)


# # Adding a reminder
# time_selected = datetime.now().time()
#
#
# def select_time(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="When do you wish to be reminded to care for your plants?",
#                              parse_mode='HTML')
#     # TODO: Generate inline query and add it to time_selected
#     return ADDPLANT
#
#
# def confirm_reminder(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="Added reminder timing: {}".format(time_selected),
#                              parse_mode='HTML')
#     uid = get_user_id(update, context)
#     add_new_timing(uid, time_selected)
#     return ConversationHandler.END
#
#
# # Adding a plant Conversation
# SELECTTIME, CONFIRMREMINDER = range(2)
#
# add_reminder_handler = ConversationHandler(
#     entry_points=[CommandHandler('add plant', add_plant)],
#     states={
#         SELECTTIME: [
#             MessageHandler(
#                 Filters.text & (~Filters.command), select_time
#             ),
#         ],
#         CONFIRMREMINDER: [
#             MessageHandler(
#                 Filters.text & (~Filters.command), confirm_reminder
#             ),
#         ],
#     },
#     # fallbacks=[CommandHandler('ready', ready), CommandHandler('cancelreg', cancel_reg)],
#     conversation_timeout=300
# )


# Reminder 1
def check_reminder(context):
    chat_ids = get_all_ids()

    for chat_id in chat_ids:
        context.bot.send_message(chat_id=chat_id, text="Time to take care of your plants!")


# Reminder 2
def check_reminder_2(context):
    chat_ids = get_all_ids()

    for chat_id in chat_ids:
        context.bot.send_message(chat_id=chat_id, text="In case you forgot to care for your plants today, please do it now!")


# Reminder 2
def thank_you(context):
    plant_name_with_id = get_all_plant_name_with_id()

    for data in plant_name_with_id:
        chat_id = data['chat_id']
        plant_name = data['plant']
        context.bot.send_message(chat_id=chat_id, text="{} thanks you for taking good care of it!".format(plant_name))


def run_bot():
    # Persistence testing
    dict_persistence = DictPersistence()

    updater = Updater(token=TOKEN, persistence=dict_persistence, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    job_queue.run_daily(check_reminder, days=(0, 1, 2, 3, 4, 5, 6), time=time(hour=12, minute=0, second=0))
    job_queue.run_daily(check_reminder_2, days=(0, 1, 2, 3, 4, 5, 6), time=time(hour=17, minute=0, second=0))

    job_queue.run_daily(thank_you, days=(0, 1, 2, 3, 4, 5, 6), time=time(hour=22, minute=0, second=0))

    dispatcher.add_handler(registration_handler)
    dispatcher.add_handler(add_plant_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)

    updater.bot.setWebhook('https://watermeplsbot.herokuapp.com/' + TOKEN)

    updater.idle()