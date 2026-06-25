import json
import os

SETTINGS_FILE = "app/config/settings.json"


def load_settings():

    default_settings = {
        "shop_name": "BarberShop",
        "theme": "Dark"
    }

    if not os.path.exists(
        SETTINGS_FILE
    ):
        save_settings(default_settings)
        return default_settings

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except:

        save_settings(default_settings)

        return default_settings

def save_settings(data):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_app_name():

    settings = load_settings()

    return settings.get(
        "shop_name",
        "BARBERSHOP"
    )