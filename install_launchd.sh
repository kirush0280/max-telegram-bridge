#!/bin/bash

# Установка MAX-Telegram Bridge как launchd сервиса (автозапуск на macOS)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.max-telegram-bridge.plist"
PLIST_SRC="$SCRIPT_DIR/$PLIST_NAME"
PLIST_DST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "=== Установка MAX-Telegram Bridge ==="
echo "Директория: $SCRIPT_DIR"

# Создаём директорию для логов
mkdir -p "$SCRIPT_DIR/logs"

# Останавливаем если уже запущен
launchctl unload "$PLIST_DST" 2>/dev/null

# Создаём plist с правильными путями
cat > "$PLIST_DST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.max-telegram-bridge</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/venv/bin/python</string>
        <string>$SCRIPT_DIR/main_pymax.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/logs/stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/logs/stderr.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF

echo "✓ Создан $PLIST_DST"

# Загружаем сервис
launchctl load "$PLIST_DST"
echo "✓ Сервис загружен"

# Проверяем статус
sleep 2
if launchctl list | grep -q "com.max-telegram-bridge"; then
    echo "✓ Сервис запущен!"
    echo ""
    echo "Логи: tail -f $SCRIPT_DIR/logs/stderr.log"
    echo "Остановить: launchctl unload ~/Library/LaunchAgents/$PLIST_NAME"
else
    echo "✗ Ошибка запуска. Проверьте логи: $SCRIPT_DIR/logs/stderr.log"
fi
