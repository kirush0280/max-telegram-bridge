import logging
from telegram import Bot
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


class TelegramClient:
    """Клиент для отправки сообщений в Telegram"""
    
    def __init__(self, token: str = TELEGRAM_BOT_TOKEN, chat_id: str = TELEGRAM_CHAT_ID):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
    
    async def send_message(self, text: str, parse_mode: str = 'HTML') -> bool:
        """Отправка текстового сообщения"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=parse_mode
            )
            logger.info(f'Сообщение отправлено в Telegram')
            return True
        except TelegramError as e:
            logger.error(f'Ошибка отправки сообщения в Telegram: {e}')
            return False
    
    def format_max_message(self, update: dict) -> str:
        """Форматирование сообщения из MAX для Telegram"""
        message = update.get('message', {})
        sender = message.get('sender', {})
        
        sender_name = sender.get('name', 'Неизвестный')
        sender_username = sender.get('username', '')
        text = message.get('body', {}).get('text', '')
        chat_type = message.get('recipient', {}).get('chat_type', 'dialog')
        
        formatted = f"<b>📨 Новое сообщение из MAX</b>\n\n"
        formatted += f"<b>От:</b> {sender_name}"
        if sender_username:
            formatted += f" (@{sender_username})"
        formatted += f"\n<b>Тип чата:</b> {chat_type}\n\n"
        formatted += f"<b>Текст:</b>\n{text}"
        
        return formatted
