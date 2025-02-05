import json
import os

from config import USERS_DATA_FILE


def load_data():
    if not os.path.exists(USERS_DATA_FILE):
        return {}
    with open(USERS_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(USERS_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_user_data(user_id, key, value):
    data = load_data()
    user_id = str(user_id)

    if user_id not in data:
        data[user_id] = {}

    data[user_id][key] = value
    save_data(data)


def load_user_data(user_id):
    """ Загружает данные пользователя из файла JSON """
    if not os.path.exists(USERS_DATA_FILE):
        return {}
    with open(USERS_DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    return users.get(str(user_id), {})


def save_user_data(user_id, key, value):
    """ Сохраняет обновлённые данные пользователя """
    users = {}
    if os.path.exists(USERS_DATA_FILE):
        with open(USERS_DATA_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)

    if str(user_id) not in users:
        users[str(user_id)] = {}

    users[str(user_id)][key] = value

    with open(USERS_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
