# Запуск Bot 2 (сигналы)

## Ошибка «No module named 'bot'»

В проекте должен быть файл **`bot.py`** в папке `signal-bot-2/`. Если его не было — он добавлен; скопируйте его на сервер вместе с остальными файлами.

## Ошибка «не находит БД» / DATABASE_URL

1. В папке **signal-bot-2** должен лежать файл **`.env`** (рядом с `main.py`, `bot.py`, `config.py`).
2. В `.env` обязательно указать:
   ```
   BOT_TOKEN=токен_второго_бота
   DATABASE_URL=postgresql://postgres.[PROJECT]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
   Строку `DATABASE_URL` скопировать из Supabase: **Connect → Connection string → Session pooler** (хост должен быть **pooler.supabase.com**, порт **6543**).

3. Запуск **обязательно из папки бота** (чтобы подхватился `.env`):
   ```bash
   cd ~/Signalbot2
   source venv/bin/activate   # если используете venv
   python3 main.py
   ```

## Локальный запуск

```bash
cd "project signals телеграмм бот/signal-bot-2"
cp .env.example .env   # затем отредактировать .env
pip install -r requirements.txt
python3 main.py
```

## Файлы, которые должны быть в signal-bot-2

- `main.py` — точка входа  
- `bot.py` — создание бота и polling  
- `config.py` — настройки  
- `database.py` — работа с БД  
- `services.py` — сервисы  
- `handlers/` — обработчики  
- `.env` — токен и DATABASE_URL (не коммитить в git)
