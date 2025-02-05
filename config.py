import os

from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.DEBUG)

aiohttp_logger = logging.getLogger("aiohttp")
aiohttp_logger.setLevel(logging.DEBUG)

load_dotenv()

USERS_DATA_FILE = "users_data.json"
API_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not API_TOKEN:
    raise NameError("API_TOKEN is missing!")
