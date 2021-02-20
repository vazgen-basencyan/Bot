from configparser import ConfigParser
import string
from random import randrange, random, choice, randint
import requests

config = ConfigParser()
config.read('config.ini')

BACKEND_URL = " http://127.0.0.1:8000/api"


def sign_up_user(user_data):
    requests.post(f"{BACKEND_URL}/reg/", data=user_data)
    return user_data


def get_auth_token(user_name, password):
    auth_data = {
        "username": user_name,
        "password": password
    }
    response = requests.post(f"{BACKEND_URL}/token-auth", data=auth_data)
    return response.json()["token"]


def create_post(auth_token):
    letters = string.ascii_lowercase
    headers = {"Authorization": f"Token {auth_token}"}
    post_data = {
        "text": "".join([letters[randrange(len(letters))] for _ in range(128)]),
    }
    requests.post(f"{BACKEND_URL}/post/", data=post_data, headers=headers)


def get_posts(auth_token):
    headers = {"Authorization": f"Token {auth_token}"}
    return requests.get(f"{BACKEND_URL}/post", headers=headers).json()


def like_post(auth_token, post_id):
    headers = {"Authorization": f"Token {auth_token}"}

    like_data = {
        "post": post_id,
        "like": "like",
    }
    requests.post(f"{BACKEND_URL}/like", data=like_data, headers=headers)


if __name__ == '__main__':
    letters = string.ascii_lowercase
    users = []
    for i in range(int(config['DEFAULT']['number_of_users'])):
        user = {
            "username": "".join([letters[randrange(len(letters))] for _ in range(6)]),
            "password": "".join([letters[randrange(len(letters))] for _ in range(6)]),
            "sex": (randint(1, 3))
        }
        sign_up_user(user_data=user)
        auth_token = get_auth_token(user["username"], user["password"])

        for _ in range(int(config['DEFAULT']['max_posts_per_user'])):
            create_post(auth_token)

        posts = get_posts(auth_token)
        posts_ids = [post["id"] for post in posts]
        for _ in range(int(config['DEFAULT']['max_likes_per_user'])):
            like_post(auth_token, choice(posts_ids))
