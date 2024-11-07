import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/postgres")
YOOKASSA_API_KEY = os.getenv("YOOKASSA_API_KEY")
SHOPLD=os.getenv("SHOPLD")
CHANNEL_ID = '@your_channel'  # Канал или группа, на который нужно проверить подписку

default_img_url = 'https://серебро.рф/img/placeholder.png'
