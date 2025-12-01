import asyncio
import logging
from pymax import MaxClient, Message
from telegram_client import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получаем номер телефона из токена или используем отдельную переменную
PHONE = os.getenv('MAX_PHONE', '+79XXXXXXXXX')  # Нужно указать номер телефона

# Инициализация клиентов
client = MaxClient(phone=PHONE, work_dir="cache", send_fake_telemetry=False)
telegram_client = TelegramClient()

# Список ID чатов для мониторинга
MONITORED_CHATS = os.getenv('MAX_CHAT_IDS', '').split(',')
MONITORED_CHATS = [int(x.strip()) for x in MONITORED_CHATS if x.strip()]


@client.on_message()
async def handle_message(message: Message) -> None:
    """Обработчик входящих сообщений"""
    try:
        chat_id = message.chat_id if hasattr(message, 'chat_id') else None
        
        # Проверяем, нужно ли обрабатывать этот чат
        if MONITORED_CHATS and chat_id not in MONITORED_CHATS:
            return
        
        # Получаем информацию о сообщении
        msg_text = message.text or ""
        
        # Получаем имя отправителя
        try:
            user = await client.get_user(message.sender)
            sender_name = user.names[0].name if user and user.names else "Неизвестный"
        except:
            sender_name = str(message.sender) if message.sender else "Неизвестный"
        
        logger.info(f'Получено сообщение от {sender_name} в чате {chat_id}: {msg_text[:50]}...')
        
        # Получаем название чата
        chat_title = "Неизвестный чат"
        for chat in client.chats:
            if chat.id == chat_id:
                chat_title = chat.title
                break
        
        # Формируем текст для Telegram
        if msg_text:
            # Экранируем HTML символы
            msg_text_escaped = msg_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            formatted_text = f"<b>📨 {sender_name}</b>\n"
            formatted_text += f"<b>Чат:</b> {chat_title}\n\n"
            formatted_text += msg_text_escaped
            
            # Отправляем в Telegram
            await telegram_client.send_message(formatted_text)
            logger.info(f'Переслано сообщение из чата {chat_id}')
            
    except Exception as e:
        logger.error(f'Ошибка обработки сообщения: {e}', exc_info=True)


@client.on_start
async def handle_start() -> None:
    """Обработчик запуска клиента"""
    logger.info('Клиент MAX запущен')
    logger.info(f'Мониторинг чатов: {MONITORED_CHATS if MONITORED_CHATS else "ВСЕ"}')
    
    # Выводим список групповых чатов
    logger.info('=== ГРУППОВЫЕ ЧАТЫ ===')
    for chat in client.chats:
        logger.info(f'  Чат: {chat.title} (ID: {chat.id})')
    
    # Выводим список диалогов (личные переписки)
    logger.info('=== ДИАЛОГИ ===')
    for dialog in client.dialogs:
        last_msg = dialog.last_message.text[:30] if dialog.last_message and dialog.last_message.text else "..."
        logger.info(f'  Диалог: {last_msg}')
    
    # Выводим список каналов
    logger.info('=== КАНАЛЫ ===')
    for channel in client.channels:
        logger.info(f'  Канал: {channel.title} (ID: {channel.id})')


async def main():
    """Главная функция"""
    logger.info('Запуск сервиса пересылки MAX → Telegram (PyMax)')
    
    try:
        await client.start()
    except KeyboardInterrupt:
        logger.info('Остановка сервиса...')
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())
