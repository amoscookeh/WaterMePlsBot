from datetime import time

from pymongo import MongoClient
import os


PASSWORD = os.environ['PASSWORD']
DATABASE = os.environ['DATABASE']
from plant import Plant
from user import User

# For data handling
client = MongoClient(
    "mongodb+srv://watermeplsbot:{}@cluster0.lwrei.mongodb.net/{}?retryWrites=true&w=majority".format(
        PASSWORD, DATABASE), ssl=True)
db = client['watermeplsdata']
user_collection = db['user_data']


def add_new_user(uid: str, name: str, chat_id: str):
    user = User(name)
    user_post = user.user_to_dict()
    user_post['_id'] = uid
    user_post['chat_id'] = chat_id
    return user_collection.insert_one(user_post)


def add_new_plant(uid: str, plant: Plant):
    plant_dict = plant.plant_to_dict()
    try:
        user_collection.find_one_and_update({'_id': uid}, {'$push': {'user_data.plants': plant_dict}})
    except Exception:
        print("Error occured while saving plant")


def add_new_timing(uid: str, timing: time):
    try:
        user_collection.find_one_and_update({'_id': uid}, {'$push': {'user_data.reminder_timings': timing}})
    except Exception:
        print("Error occured while saving new timing")


def get_all_ids():
    search = user_collection.find().distinct('chat_id')
    chat_ids = []
    for id in search:
        chat_ids.append(id)
    return chat_ids


def get_all_plant_name_with_id():
    search = user_collection.find()
    plant_name_with_id = []

    for doc in search:
        plant_name_with_id.append(
            {
                'chat_id': doc['chat_id'],
                'plant': doc['plants']['name']
            }
        )

    return plant_name_with_id