# MAX → Telegram Bridge

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Сервис для автоматической пересылки сообщений из мессенджера [MAX](https://max.ru) в Telegram.

## Возможности

- 📨 Пересылка сообщений из выбранных чатов MAX в Telegram
- 🔄 Автоматическое переподключение при потере связи
- 🚀 Простая интерактивная настройка
- 🖥️ Автозапуск при загрузке системы (macOS / Linux)

## Требования

- Python 3.10+
- Аккаунт в MAX
- Telegram бот (создаётся через [@BotFather](https://t.me/BotFather))

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/kirush0280/max-telegram-bridge.git
cd max-telegram-bridge

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

## Настройка

Запустите интерактивную настройку:

```bash
python setup.py
```

Скрипт запросит:
1. **Токен Telegram бота** — получите у [@BotFather](https://t.me/BotFather)
2. **ID чата Telegram** — куда пересылать сообщения (узнать через [@userinfobot](https://t.me/userinfobot))
3. **Номер телефона MAX** — для авторизации
4. **Код из SMS** — при первом запуске
5. **Выбор чатов** — какие чаты MAX мониторить

## Запуск

```bash
./venv/bin/python main_pymax.py
```

---

## Автозапуск

### macOS (launchd)

```bash
./install_launchd.sh
```

**Управление сервисом:**

```bash
# Логи
tail -f logs/stderr.log

# Остановить
launchctl unload ~/Library/LaunchAgents/com.max-telegram-bridge.plist

# Запустить
launchctl load ~/Library/LaunchAgents/com.max-telegram-bridge.plist

# Перезапустить
launchctl unload ~/Library/LaunchAgents/com.max-telegram-bridge.plist && \
launchctl load ~/Library/LaunchAgents/com.max-telegram-bridge.plist
```

### Linux (systemd)

```bash
./install_systemd.sh
```

**Управление сервисом:**

```bash
# Логи
tail -f logs/stderr.log
# или
sudo journalctl -u max-telegram-bridge -f

# Остановить
sudo systemctl stop max-telegram-bridge

# Запустить
sudo systemctl start max-telegram-bridge

# Перезапустить
sudo systemctl restart max-telegram-bridge

# Статус
sudo systemctl status max-telegram-bridge

# Отключить автозапуск
sudo systemctl disable max-telegram-bridge
```

---

## Структура проекта

```
├── main_pymax.py              # Основной скрипт
├── setup.py                   # Интерактивная настройка
├── telegram_client.py         # Клиент Telegram
├── config.py                  # Загрузка конфигурации
├── requirements.txt           # Зависимости
├── .env.example               # Пример конфигурации
├── install_launchd.sh         # Автозапуск macOS
├── install_systemd.sh         # Автозапуск Linux
└── logs/                      # Логи сервиса
```

## Изменение настроек

Для изменения списка чатов или других параметров:

```bash
python setup.py
```

Или отредактируйте `.env` вручную и перезапустите сервис.

## Лицензия

MIT License

## Благодарности

- [pymax](https://github.com/ink-developer/PyMax) — Python библиотека для MAX
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — Telegram Bot API
