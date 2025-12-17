import json
import os

USERS_FILE = "data/users.json"


# ---------- HELPERS ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# ---------- AUTH ----------
def authenticate(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None


def create_user(username, password, role="user"):
    users = load_users()
    if username in users:
        return False

    users[username] = {
        "password": password,
        "role": role
    }
    save_users(users)
    return True


def change_password(username, old_password, new_password):
    users = load_users()
    if username in users and users[username]["password"] == old_password:
        users[username]["password"] = new_password
        save_users(users)
        return True
    return False
