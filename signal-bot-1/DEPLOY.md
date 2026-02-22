# Хостинг бота на сервере

## Какие файлы загружать на сервер

Загрузите **только** эти файлы и папки (без папки `venv` и без `.git`):

```
project/
├── main.py              # точка входа (запуск: python3 main.py)
├── bot.py               # логика бота
├── config.py            # настройки из .env
├── database.py          # работа с БД
├── services.py          # Crypto Pay, админы, пользователи
├── requirements.txt     # зависимости Python
├── .env                 # секреты (создать на сервере из .env.example)
├── handlers/
│   ├── __init__.py
│   ├── admin.py
│   ├── start.py
│   └── payment.py
```

Если в проекте есть файл **`chat_cleanup.py`** в корне — его тоже нужно загрузить.

Файл **`.env`** на сервер не копируйте с компьютера (в нём могут быть локальные пути). Создайте его на сервере вручную и заполните переменные (см. ниже).

---

## Что нужно установить на сервере

### 1. Python

- **Python 3.10, 3.11 или 3.12**

Проверка:
```bash
python3 --version
```

Установка (если нет):
- **Ubuntu/Debian:** `sudo apt update && sudo apt install python3 python3-pip python3-venv`
- **CentOS:** `sudo yum install python3 python3-pip`

### 2. Зависимости проекта (что «скачать»)

На сервере в папке с ботом выполните:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac; на Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Будут установлены пакеты из **requirements.txt**:
- `aiogram==3.3.0` — работа с Telegram Bot API
- `requests==2.31.0` — запросы к Crypto Pay API
- `python-dotenv==1.0.0` — загрузка переменных из `.env`

SQLite уже встроен в Python, отдельно ставить не нужно.

---

## Файл .env на сервере

Создайте в корне проекта файл **`.env`** и заполните (можно скопировать из `.env.example` и подставить свои значения):

```env
BOT_TOKEN=123456:ABC...          # токен от @BotFather
ADMIN_IDS=123456789              # ваш Telegram ID (через запятую, если админов несколько)
DATABASE_URL=sqlite:///./bot.db
CRYPTO_BOT_TOKEN=                 # токен Crypto Pay от @CryptoBot
CRYPTO_PAY_TESTNET=false          # true — для тестовой сети
REVIEWS_CHANNEL=https://t.me/...
OPERATOR_USERNAME=ecoTomSawyer
SIGNALS_CHANNEL=
LANDING_URL=
PRODUCT_CHANNEL=
LOG_LEVEL=INFO
DEBUG=False
```

Обязательно укажите **BOT_TOKEN** и **ADMIN_IDS**.

---

## Запуск на сервере

```bash
cd /путь/к/папке/бота
source venv/bin/activate
python3 main.py
```

Чтобы бот работал в фоне и не падал при отключении SSH, используйте **systemd** или **screen**/ **tmux**.

### Пример systemd (постоянный запуск)

Файл `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Signals Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/telegram-bot
ExecStart=/home/ubuntu/telegram-bot/venv/bin/python3 main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Команды:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

---

## Краткий чек-лист

| Действие | Команда/файл |
|----------|---------------|
| Загрузить файлы | Все `.py`, `requirements.txt`, папка `handlers/`, без `venv` |
| Создать .env | Скопировать из `.env.example`, заполнить BOT_TOKEN и ADMIN_IDS |
| Установить Python | `python3 --version` (3.10+) |
| Создать venv | `python3 -m venv venv` |
| Установить зависимости | `pip install -r requirements.txt` |
| Запуск | `python3 main.py` |
| Запуск в фоне | systemd или `screen`/`tmux` |

После первого запуска в папке появится файл **bot.db** (база SQLite) — его можно бэкапить и при переезде сервера копировать вместе с проектом.
