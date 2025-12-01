#!/usr/bin/env python3
"""
Интерактивная настройка MAX → Telegram Bridge
"""

import asyncio
import os
from pathlib import Path

# Проверяем наличие .env
ENV_FILE = Path('.env')


def create_env_file():
    """Создаёт базовый .env файл"""
    if not ENV_FILE.exists():
        ENV_FILE.write_text("""# Telegram Bot
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# MAX
MAX_PHONE=

# Чаты MAX для мониторинга (заполняется автоматически)
MAX_CHAT_IDS=
""")


def update_env(key: str, value: str):
    """Обновляет значение в .env файле"""
    if not ENV_FILE.exists():
        create_env_file()
    
    content = ENV_FILE.read_text()
    lines = content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith(f'{key}='):
            lines[i] = f'{key}={value}'
            updated = True
            break
    
    if not updated:
        lines.append(f'{key}={value}')
    
    ENV_FILE.write_text('\n'.join(lines))


def get_env(key: str) -> str:
    """Получает значение из .env файла"""
    if not ENV_FILE.exists():
        return ''
    
    for line in ENV_FILE.read_text().split('\n'):
        if line.startswith(f'{key}='):
            return line.split('=', 1)[1].strip()
    return ''


async def setup_telegram():
    """Настройка Telegram"""
    print("\n=== Настройка Telegram ===\n")
    
    current_token = get_env('TELEGRAM_BOT_TOKEN')
    if current_token:
        print(f"Текущий токен бота: {current_token[:20]}...")
        change = input("Изменить? (y/N): ").strip().lower()
        if change != 'y':
            token = current_token
        else:
            token = input("Введите токен Telegram бота: ").strip()
    else:
        token = input("Введите токен Telegram бота: ").strip()
    
    if token:
        update_env('TELEGRAM_BOT_TOKEN', token)
    
    current_chat = get_env('TELEGRAM_CHAT_ID')
    if current_chat:
        print(f"Текущий чат ID: {current_chat}")
        change = input("Изменить? (y/N): ").strip().lower()
        if change != 'y':
            chat_id = current_chat
        else:
            chat_id = input("Введите ID чата/канала Telegram: ").strip()
    else:
        chat_id = input("Введите ID чата/канала Telegram: ").strip()
    
    if chat_id:
        update_env('TELEGRAM_CHAT_ID', chat_id)
    
    print("✓ Telegram настроен")


async def setup_max():
    """Настройка MAX и выбор чатов"""
    print("\n=== Настройка MAX ===\n")
    
    current_phone = get_env('MAX_PHONE')
    if current_phone:
        print(f"Текущий номер: {current_phone}")
        change = input("Изменить? (y/N): ").strip().lower()
        if change != 'y':
            phone = current_phone
        else:
            phone = input("Введите номер телефона MAX (+7...): ").strip()
    else:
        phone = input("Введите номер телефона MAX (+7...): ").strip()
    
    if phone:
        update_env('MAX_PHONE', phone)
    
    # Подключаемся к MAX для получения списка чатов
    print("\nПодключение к MAX...")
    
    from pymax import MaxClient
    
    client = MaxClient(phone=phone, work_dir="cache", send_fake_telemetry=False)
    
    try:
        # Запускаем клиент (может потребоваться код)
        await client.start()
        
        # Ждём синхронизации
        await asyncio.sleep(2)
        
        # Показываем список чатов
        print("\n=== Доступные чаты ===\n")
        
        chats = list(client.chats)
        if not chats:
            print("Нет доступных групповых чатов")
            await client.close()
            return
        
        for i, chat in enumerate(chats, 1):
            print(f"  {i}. {chat.title}")
        
        print(f"\n  0. Все чаты")
        print()
        
        # Выбор чатов
        selection = input("Выберите чаты для мониторинга (номера через запятую, например: 1,2): ").strip()
        
        if selection == '0' or selection == '':
            selected_ids = []
            print("✓ Будут мониториться ВСЕ чаты")
        else:
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                selected_ids = []
                selected_names = []
                for idx in indices:
                    if 1 <= idx <= len(chats):
                        selected_ids.append(str(chats[idx - 1].id))
                        selected_names.append(chats[idx - 1].title)
                
                print(f"✓ Выбраны чаты: {', '.join(selected_names)}")
            except ValueError:
                print("Ошибка ввода, будут мониториться все чаты")
                selected_ids = []
        
        update_env('MAX_CHAT_IDS', ','.join(selected_ids))
        
        await client.close()
        
    except Exception as e:
        print(f"Ошибка: {e}")
        try:
            await client.close()
        except:
            pass


async def test_connection():
    """Тестирование подключения"""
    print("\n=== Тест подключения ===\n")
    
    # Тест Telegram
    print("Проверка Telegram...")
    try:
        from telegram_client import TelegramClient
        tg = TelegramClient()
        await tg.send_message("🧪 Тест подключения MAX → Telegram Bridge")
        print("✓ Telegram работает")
    except Exception as e:
        print(f"✗ Ошибка Telegram: {e}")
    
    print("\n✓ Настройка завершена!")
    print("\nДля запуска сервиса выполните:")
    print("  ./venv/bin/python main_pymax.py")
    print("\nДля автозапуска (macOS):")
    print("  ./install_launchd.sh")


async def main():
    print("=" * 50)
    print("  MAX → Telegram Bridge - Настройка")
    print("=" * 50)
    
    create_env_file()
    
    await setup_telegram()
    await setup_max()
    await test_connection()


if __name__ == '__main__':
    asyncio.run(main())
