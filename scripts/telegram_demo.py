from pyrogram import Client
from dotenv import load_dotenv
import os 

load_dotenv()
CONFIG = {
    "telegram_api_id": int(os.getenv("TG_API_ID")),
    "telegram_hash": os.getenv("TG_API_HASH"),
}
app = Client("my_account",CONFIG['telegram_api_id'],CONFIG['telegram_hash'])
with app:
    app.send_message(+251986938129,"Hello from python package 2")
