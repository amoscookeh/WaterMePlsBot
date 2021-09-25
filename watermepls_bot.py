from datetime import datetime, time
from random import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, InlineQueryHandler, \
    CallbackQueryHandler, DictPersistence
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import logging
import os

from feedback import Feedback
from helper import get_user_id, get_chat_id, get_today_midnight
from plant import Plant
from watermepls_mongo import add_new_user, add_new_plant, add_new_timing, get_all_ids, get_all_plant_name_with_id, \
    check_existing_user, add_new_feedback
from weather_api import get_weather_forecast, get_weather_msg

PORT = int(os.environ.get('PORT', 8443))
TOKEN = os.environ['TOKEN']

# For logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# First time starting the bot
def start(update, context):
    uid = get_user_id(update, context)
    existing_user = check_existing_user(uid)

    if existing_user:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Welcome to WaterMePlsBot 💦🪴 [Beta Test Version]!",
                                 parse_mode='HTML')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="It seems like you're already a part of this family! Use /edit_user to change your name")
        return ConversationHandler.END

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to WaterMePlsBot 💦🪴 [Beta Test Version]!",
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
                             text="Thanks {} for joining the WaterMePls 💦🪴 community!\n\nlet's start by adding your "
                                  "plants!\n\nUse /add_plant to invite some plant friends to the fam!".format(name))
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
                             text="Time to add a plant 🌲🌳🌴🍀🎍🪴! \nFirstly, what type of plant is this? (Eg. Sunflower, "
                                  "Cactus, etc.)",
                             parse_mode='HTML')
    return ADDPLANT


def ask_for_plant_name(update, context):
    plant_type = update.message.text
    new_plant.set_type(plant_type)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="What is your name for this plant? (Research has shown that naming your plant makes "
                                  "it 5x healthier!)",
                             parse_mode='HTML')
    return REGISTERPLANT


def register_plant(update, context):
    plant_name = update.message.text
    new_plant.set_name(plant_name)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Confirm addition? Use /cancel to stop this process".format(
                                 new_plant.name),
                             parse_mode='HTML')
    return SAVEPLANT


def save_plant(update, context):
    uid = get_user_id(update, context)
    add_new_plant(uid, new_plant)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="We welcome {} to the family✨! Let's work together to take good care of it💚!".format(
                                 new_plant.name),
                             parse_mode='HTML')
    return ConversationHandler.END


# Adding a plant Conversation
ADDPLANT, REGISTERPLANT, SAVEPLANT = range(3)

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
        SAVEPLANT: [
            MessageHandler(
                Filters.text & (~Filters.command), save_plant
            ),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    conversation_timeout=300
)


def about_us(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I see that you're curious about the creators of WaterMePlsBot!\n\nabout -> Find "
                                  "out more about this bot!\n\nfeedback -> Give us some feedback!\n\nWell, "
                                  "How can I help you? Type the option you want to continue! ")
    return WHAT_TO_DO


def re_route(update, context):
    if update.message.text == 'about':
        return about(update, context)
    elif update.message.text == 'feedback':
        return ask_for_feedback(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Did not get that... Type either <about> or <feedback>")
        return WHAT_TO_DO


def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to 💦WaterMePlsBot💦! This bot was built for the sole purpose of making"
                                  " plant care a habit for all you young aspiring plant parents 💚"
                                  "\n\nProudly brought to you by the creator of @PayMePls_Bot and @WeirdTalkBot")
    return ConversationHandler.END


def ask_for_feedback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Over here in the WaterMePls community, we care about what our users think")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="So... How has your experience been?")
    return FEEDBACK


new_feedback = Feedback(None, None)


def feedback(update, context):
    new_feedback.user_experience = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Thanks for letting me know!")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Well, to help me improve, do you have any feature ideas or general feedback you'd "
                                  "like to give?")
    return IDEAS


def ideas(update, context):
    new_feedback.feedback = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I appreciate that!")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Well, thank you once again for trying to help WaterMePlsBot improve! This matters "
                                  "alot to me and let us help more people become capable Plant Parents!")

    add_new_feedback(update.effective_chat.id, new_feedback.user_experience, new_feedback.feedback)

    # Send this feedback to myself
    context.bot.send_message(chat_id="26206762",
                             text="WaterMePlsBot Feedback from {}:\n\nExperience: {}\n\nIdeas/Feedback: {}".format(
                                 update.effective_chat.id, new_feedback.user_experience, new_feedback.feedback))

    return ConversationHandler.END


# About us Login Conversation
WHAT_TO_DO, FEEDBACK, IDEAS = range(3)

about_us_handler = ConversationHandler(
    entry_points=[CommandHandler('about_us', about_us)],
    states={
        WHAT_TO_DO: [
            MessageHandler(
                Filters.text & (~Filters.command), re_route
            )
        ],
        FEEDBACK: [
            MessageHandler(
                Filters.text & (~Filters.command), feedback
            )
        ],
        IDEAS: [
            MessageHandler(
                Filters.text & (~Filters.command), ideas
            )
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    conversation_timeout=300
)


def edit_user(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="What would you like to change your name to?")
    return DONE


def user_name_changed(update, context):
    new_name = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Okie dokie! I will now remember you as {}!".format(new_name))
    return ConversationHandler.END


# Change username Conversation
DONE = range(1)

edit_user_handler = ConversationHandler(
    entry_points=[CommandHandler('edit_user', edit_user)],
    states={
        DONE: [
            MessageHandler(
                Filters.text & (~Filters.command), user_name_changed
            )
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
reminder_messages = [
    "Time to care for your 🪴plants🪴!",
    "Your plants need your 🥰attention🥰!",
    "If Rais can do it, you can too✨! Go check on your plants today!",
    "If you have time to 😴nap😴, you have time to care for your plants. Do it now!",
    '"Wussup, come hang with me! 🥺🥺🥺" -Mr. Plant & Gang',
    '"Bro... Im dying of thirst... 🤢🤢🤢" -Mr. Plant',
    "Sing your plants a 🎶song🎶! It makes both of you happier!\nFun fact: Ngee Feng's goto song to sing is 🦜Mockingbird🦜!",
    "Have a break, go hang with your 🪴plants🪴!"
]


def check_reminder(context):
    total_num_of_msgs = len(reminder_messages)
    reminder_msg_inx = random.randint(0, total_num_of_msgs - 1)
    msg_of_the_day = reminder_messages[reminder_msg_inx]
    chat_ids = get_all_ids()

    for chat_id in chat_ids:
        context.bot.send_message(chat_id=chat_id, text=msg_of_the_day)


# Reminder 2
reminder2_messages = [
    "In case you ignored my earlier message... It's time to care for your 🪴plants🪴!",
    "Plants without 🥰attention🥰 are 🥺sad🥺 plants!",
    "Have you watered your 💦plants💦 today? It sure is a dry day...",
    "If you have time to 😴nap😴, you have time to care for your plants. Do it now!",
    'Plant. Need. Attention. Now.',
    "Have a break, go hang with your 🪴plants🪴!"
]


def check_reminder_2(context):
    total_num_of_msgs = len(reminder2_messages)
    reminder_msg_inx = random.randint(0, total_num_of_msgs - 1)
    msg_of_the_day = reminder2_messages[reminder_msg_inx]
    chat_ids = get_all_ids()

    for chat_id in chat_ids:
        context.bot.send_message(chat_id=chat_id, text=msg_of_the_day)


# Reminder 2
thank_you_messages = [
    "You make me a happy and healthy plant!\n\n And I can't thank you enough for that <333",
    "Hanging out with you today has been lit! See you tmr!",
    "A plant and human friendship is always magical✨!",
    "Thanks for your hardwork today... Goodnight and rest well😴😴😴!",
    'U r such a sweet Plant Parent 🥺🥺🥺',
    "Thanks for your hardwork today... Maybe tomorrow you could sing me a 🎶song🎶? My goto song would be 🦜Mockingbird🦜!",
    "Thanks for giving me life🪴!"
]


def thank_you(context):
    plant_name_with_id = get_all_plant_name_with_id()

    total_num_of_msgs = len(thank_you_messages)
    thank_you_messages_idx = random.randint(0, total_num_of_msgs - 1)
    msg_of_the_day = reminder2_messages[thank_you_messages_idx]

    for data in plant_name_with_id:
        chat_id = data['chat_id']
        plant_name = data['plant']
        context.bot.send_message(chat_id=chat_id,
                                 text="Dear Plant Parent,\n\n{}\n\nLove, 💚{}💚".format(plant_name, msg_of_the_day))


def check_weather(context):
    weather_string = get_weather_forecast('Clementi')
    message = get_weather_msg(weather_string)

    if message is not None:
        chat_ids = get_all_ids()
        for chat_id in chat_ids:
            context.bot.send_message(chat_id=chat_id, text=message)
    else:
        context.bot.send_message(chat_id="26206762", text=weather_string)


def weather_2h(update, context):
    weather_string = get_weather_forecast('Clementi')

    context.bot.send_message(chat_id=update.effective_chat.id, text="Latest weather updates: {}".format(weather_string))


def run_bot():
    # Persistence testing
    dict_persistence = DictPersistence()

    updater = Updater(token=TOKEN, persistence=dict_persistence, use_context=True)
    dispatcher = updater.dispatcher

    job_queue = updater.job_queue

    job_queue.run_daily(check_reminder, days=(0, 1, 2, 3, 4, 5, 6), time=time(hour=4, minute=0, second=0))  # Reminder 1
    job_queue.run_daily(check_reminder_2, days=(0, 1, 2, 3, 4, 5, 6),
                        time=time(hour=9, minute=0, second=0))  # Reminder 2
    job_queue.run_daily(thank_you, days=(0, 1, 2, 3, 4, 5, 6), time=time(hour=14, minute=0, second=0))  # Thank you
    job_queue.run_repeating(check_weather, interval=7200, first=60)  # Weather
    job_queue.start()

    jobs = job_queue.jobs()
    for job in jobs:
        print(job.next_t.tzname())
        print(job.next_t)

    dispatcher.add_handler(registration_handler)
    dispatcher.add_handler(add_plant_handler)
    dispatcher.add_handler(about_us_handler)
    dispatcher.add_handler(edit_user_handler)
    dispatcher.add_handler(CommandHandler('weather2h', weather_2h))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://watermeplsbot.herokuapp.com/' + TOKEN)

    updater.idle()
