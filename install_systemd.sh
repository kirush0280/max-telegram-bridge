#!/bin/bash

# Установка MAX-Telegram Bridge как systemd сервиса (автозапуск на Linux)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_NAME="max-telegram-bridge"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
CURRENT_USER=$(whoami)

echo "=== Установка MAX-Telegram Bridge (Linux) ==="
echo "Директория: $SCRIPT_DIR"
echo "Пользователь: $CURRENT_USER"

# Создаём директорию для логов
mkdir -p "$SCRIPT_DIR/logs"

# Проверяем наличие venv
if [ ! -f "$SCRIPT_DIR/venv/bin/python" ]; then
    echo "✗ Ошибка: виртуальное окружение не найдено"
    echo "  Выполните: python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Создаём systemd service файл
sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=MAX to Telegram Bridge
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$SCRIPT_DIR
ExecStart=$SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/main_pymax.py
Restart=always
RestartSec=10
StandardOutput=append:$SCRIPT_DIR/logs/stdout.log
StandardError=append:$SCRIPT_DIR/logs/stderr.log

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Создан $SERVICE_FILE"

# Перезагружаем systemd
sudo systemctl daemon-reload
echo "✓ Systemd перезагружен"

# Включаем и запускаем сервис
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

# Проверяем статус
sleep 2
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "✓ Сервис запущен!"
    echo ""
    echo "Логи: tail -f $SCRIPT_DIR/logs/stderr.log"
    echo "      или: sudo journalctl -u $SERVICE_NAME -f"
    echo ""
    echo "Управление:"
    echo "  sudo systemctl stop $SERVICE_NAME"
    echo "  sudo systemctl start $SERVICE_NAME"
    echo "  sudo systemctl restart $SERVICE_NAME"
    echo "  sudo systemctl status $SERVICE_NAME"
else
    echo "✗ Ошибка запуска. Проверьте:"
    echo "  sudo systemctl status $SERVICE_NAME"
    echo "  sudo journalctl -u $SERVICE_NAME"
fi
