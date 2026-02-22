# Запуск бота на сервере

После того как файлы перенесены на сервер.

---

## 1. Подключиться к серверу и перейти в папку бота

```bash
ssh user@your-server-ip
cd /path/to/signal-bot-1
```

(Замените `user`, `your-server-ip` и путь на свои.)

---

## 2. Создать виртуальное окружение и установить зависимости

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Создать файл .env

Создайте файл `.env` в папке бота (скопируйте с `.env.example` или создайте вручную) и заполните:

- `BOT_TOKEN` — токен от @BotFather  
- `ADMIN_IDS` — ваш Telegram ID  
- `DATABASE_URL` — строка подключения Supabase (postgresql://...pooler.supabase.com...)  
- Остальные переменные по необходимости (Crypto Pay, каналы и т.д.)

---

## 4. Запуск

**Один раз (в текущем терминале):**

```bash
source venv/bin/activate
python3 main.py
```

Бот будет работать, пока открыт терминал. Закрытие SSH или выход из терминала остановит бота.

---

## 5. Запуск в фоне (чтобы работал после отключения)

**Вариант A — screen**

```bash
screen -S bot1
source venv/bin/activate
python3 main.py
```

Отключиться от сессии: `Ctrl+A`, затем `D`.  
Вернуться к боту: `screen -r bot1`.

**Вариант B — nohup**

```bash
source venv/bin/activate
nohup python3 main.py > bot.log 2>&1 &
```

Логи будут в `bot.log`. Остановить: `pkill -f "python3 main.py"` (из папки бота).

**Вариант C — systemd (рекомендуется для постоянной работы)**

Создайте файл `/etc/systemd/system/signal-bot-1.service`:

```ini
[Unit]
Description=Signal Bot 1
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/signal-bot-1
ExecStart=/path/to/signal-bot-1/venv/bin/python3 main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Замените `YOUR_USER` и пути. Затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable signal-bot-1
sudo systemctl start signal-bot-1
sudo systemctl status signal-bot-1
```

Логи: `journalctl -u signal-bot-1 -f`

---

## Кратко

```bash
cd /path/to/signal-bot-1
source venv/bin/activate
python3 main.py
```

Для фона: `screen` или `nohup ... &` или systemd.
