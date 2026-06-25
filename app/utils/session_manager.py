import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SESSION_FILE = os.path.join(
    BASE_DIR,
    "config",
    "session.json"
)


def save_session(username):

    with open(
        SESSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "username": username
            },
            file
        )


def load_session():

    if not os.path.exists(
        SESSION_FILE
    ):
        return None

    with open(
        SESSION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data.get(
        "username"
    )


def clear_session():

    with open(
        SESSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {},
            file
        )