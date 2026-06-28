import logging

from pyrogram import Client

from config import API_HASH, API_ID, SESSION_STRING, BOT_TOKEN

FORMAT = "[UB]:%(message)s"

logging.basicConfig(level=logging.INFO,handlers=[logging.FileHandler('logs.txt'),
                                                 logging.StreamHandler()],format=FORMAT)

ub = Client("ub",
    api_id= API_ID,
    api_hash= API_HASH,
    session_string= SESSION_STRING,
    plugins=dict(root = "ronova.plugins.user")
)
bot = Client("app",
    api_id= API_ID,
    api_hash= API_HASH,
    bot_token= BOT_TOKEN,
    plugins=dict(root = "ronova.plugins.bot")
)