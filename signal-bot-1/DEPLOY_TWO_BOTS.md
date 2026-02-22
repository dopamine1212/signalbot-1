# Запуск двух ботов на одном сервере

Подходит для любого VPS/хостинга (включая бесплатный). Домен не нужен.

---

## Шаг 1. Загрузить файлы на сервер

Создайте две папки, например в домашнем каталоге:

- **SignalBot1** — файлы первого бота (main.py, bot.py, config.py, database.py, services.py, requirements.txt, папка handlers/, файл .env создадите на сервере).
- **SignalBot2** — файлы второго бота (main.py, bot.py, config.py, database.py, services.py, requirements.txt, папка handlers/, .env на сервере).

Папку **venv** с компьютера не копируйте — её создадите на сервере.

---

## Шаг 2. Первый бот (SignalBot1)

```bash
cd ~/SignalBot1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создайте файл **.env** в этой же папке (nano .env) и заполните:

- BOT_TOKEN=токен_первого_бота
- ADMIN_IDS=ваш_telegram_id
- DATABASE_URL=postgresql://...ваша_строка_supabase...
- Остальные переменные по необходимости (Crypto Pay, каналы и т.д.)

Проверка запуска (остановите через Ctrl+C):

```bash
source venv/bin/activate
python3 main.py
```

---

## Шаг 3. Второй бот (SignalBot2)

В **новом** терминале (или после выхода из первого):

```bash
cd ~/SignalBot2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создайте **.env** в SignalBot2:

- BOT_TOKEN=токен_второго_бота
- ADMIN_IDS=те_же_что_у_первого
- DATABASE_URL=та_же_строка_что_у_первого_бота

Проверка:

```bash
source venv/bin/activate
python3 main.py
```

---

## Шаг 4. Запустить обоих и не закрывать консоль

**Вариант A — в фоне (одна консоль)**

В одной сессии выполните по очереди:

```bash
cd ~/SignalBot1 && source venv/bin/activate && nohup python3 main.py > ~/bot1.log 2>&1 &
cd ~/SignalBot2 && source venv/bin/activate && nohup python3 main.py > ~/bot2.log 2>&1 &
```

Оба бота будут работать в фоне. Логи:
- Бот 1: `tail -f ~/bot1.log`
- Бот 2: `tail -f ~/bot2.log`

Остановить:
- Бот 1: `pkill -f "SignalBot1/main.py"`
- Бот 2: `pkill -f "SignalBot2/main.py"`

**Вариант B — screen (две сессии, логи в консоли)**

```bash
screen -S bot1
cd ~/SignalBot1 && source venv/bin/activate && python3 main.py
# Отсоединиться: Ctrl+A, затем D

screen -S bot2
cd ~/SignalBot2 && source venv/bin/activate && python3 main.py
# Отсоединиться: Ctrl+A, затем D
```

Подключиться к логам: `screen -r bot1` или `screen -r bot2`. Выход без остановки: Ctrl+A, D.

**Вариант C — systemd (если есть root/sudo)**

Создайте два сервиса (пути и пользователя замените на свои):

```bash
sudo nano /etc/systemd/system/signal-bot-1.service
```

```ini
[Unit]
Description=Signal Bot 1
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/SignalBot1
ExecStart=/root/SignalBot1/venv/bin/python3 main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Аналогично **signal-bot-2.service** для SignalBot2. Затем:

```bash
sudo systemctl daemon-reload
sudo systemctl enable signal-bot-1 signal-bot-2
sudo systemctl start signal-bot-1 signal-bot-2
```

---

## Чек-лист

| Действие | Бот 1 | Бот 2 |
|----------|--------|--------|
| Папка на сервере | ~/SignalBot1 | ~/SignalBot2 |
| venv | cd SignalBot1 && python3 -m venv venv | cd SignalBot2 && python3 -m venv venv |
| pip install | pip install -r requirements.txt | то же |
| .env | BOT_TOKEN, DATABASE_URL, ADMIN_IDS… | другой BOT_TOKEN, тот же DATABASE_URL, те же ADMIN_IDS |
| Запуск | nohup/screen/systemd | nohup/screen/systemd |

Оба бота используют одну базу Supabase (один и тот же DATABASE_URL в .env).
