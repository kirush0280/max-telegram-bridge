import os
from dotenv import load_dotenv

load_dotenv()

MAX_API_TOKEN = os.getenv('MAX_API_TOKEN')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
ADMIN_TELEGRAM_ID = os.getenv('ADMIN_TELEGRAM_ID')
MAX_CHAT_IDS = os.getenv('MAX_CHAT_IDS', '')
MONITOR_ENABLED = os.getenv('MONITOR_ENABLED', 'true').lower() == 'true'
MODE = os.getenv('MODE', 'polling')
