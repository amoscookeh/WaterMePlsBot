from datetime import time

from pymongo import MongoClient
import os

from feedback import Feedback

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
feedback_collection = db['feedback']


def add_new_user(uid: str, name: str, chat_id: str):
    user = User(name)
    user_post = user.user_to_dict()
    user_post['_id'] = uid
    user_post['chat_id'] = chat_id
    return user_collection.insert_one(user_post)


def check_existing_user(uid: str):
    return user_collection.find({'_id': uid}).count() > 0



def add_new_plant(uid: str, plant: Plant):
    print("_id: " + uid)
    plant_dict = plant.plant_to_dict()
    try:
        user_collection.find_one_and_update({'_id': uid}, {'$push': {'plants': plant_dict}})
    except Exception:
        print("Error occured while saving plant")


def add_new_timing(uid: str, timing: time):
    try:
        user_collection.find_one_and_update({'_id': uid}, {'$push': {'reminder_timings': timing}})
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
                'plant': doc['plants'][0]['name']
            }
        )

    return plant_name_with_id


def add_new_feedback(uid: str, user_experience: str, user_feedback: str):
    new_feedback = Feedback(user_experience, user_feedback)
    new_post = new_feedback.feedback_to_dict()
    new_post['_id'] = uid
    return feedback_collection.insert_one(new_post)


def edit_username(uid: str, new_name: str):
    return user_collection.find_one_and_update({'_id': uid}, {'$set': {'name': new_name}})