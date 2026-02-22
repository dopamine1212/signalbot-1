#!/bin/bash
# Запуск обоих ботов на одном сервере без зависаний.
# Использование: chmod +x start_both_bots.sh && ./start_both_bots.sh

set -e
BOT1_DIR="${BOT1_DIR:-$HOME/SignalBot1}"
BOT2_DIR="${BOT2_DIR:-$HOME/Signalbot2}"
LOG1="${LOG1:-$HOME/bot1.log}"
LOG2="${LOG2:-$HOME/bot2.log}"
START_DELAY=5

# -u = небуферизованный вывод (логи сразу в файл, видно где зависло)
PYTHON_CMD="python3 -u main.py"

echo "Запуск Bot 1: $BOT1_DIR"
(cd "$BOT1_DIR" && source venv/bin/activate && nohup $PYTHON_CMD >> "$LOG1" 2>&1 &)
echo "Ожидание ${START_DELAY} сек, чтобы БД не принимала два подключения сразу..."
sleep "$START_DELAY"

echo "Запуск Bot 2: $BOT2_DIR"
(cd "$BOT2_DIR" && source venv/bin/activate && nohup $PYTHON_CMD >> "$LOG2" 2>&1 &)

echo ""
echo "Оба бота запущены в фоне."
echo "  Лог Bot 1: tail -f $LOG1"
echo "  Лог Bot 2: tail -f $LOG2"
echo "  Остановить Bot 1: pkill -f \"SignalBot1.*main.py\""
echo "  Остановить Bot 2: pkill -f \"Signalbot2.*main.py\""
