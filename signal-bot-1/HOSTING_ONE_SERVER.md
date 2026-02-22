# Лендинг + два бота на одном сервере

На одном VPS можно запустить:
1. **Лендинг** — сайт (HTML или статика).
2. **Бот 1** (SignalBot1) — главный бот.
3. **Бот 2** (SignalBot2) — бот с сигналами.

---

## 1. Что где будет

| Компонент   | Как работает | Порт (если нужен) |
|------------|--------------|--------------------|
| Лендинг    | Nginx раздаёт файлы или проксирует на приложение | 80, 443 |
| Бот 1      | Процесс `python3 main.py` (polling, порт не нужен) | — |
| Бот 2      | Процесс `python3 main.py` (polling) | — |

Боты к Telegram подключаются сами, входящие порты им не нужны. Открыть снаружи нужно только 80/443 для лендинга.

---

## 2. Сервер

- Любой VPS (Ubuntu 22.04, Debian и т.п.).
- **Домен не нужен** — лендинг можно открывать по IP: `http://IP-вашего-сервера`.

---

## 3. Лендинг (Nginx + статика)

### Установка Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

### Папка для лендинга

```bash
sudo mkdir -p /var/www/landing
# Загрузите сюда файлы лендинга: index.html, css, js, картинки
# Права:
sudo chown -R www-data:www-data /var/www/landing
```

### Конфиг Nginx для лендинга (без домена — по IP)

```bash
sudo nano /etc/nginx/sites-available/landing
```

Вставьте (лендинг будет открываться по адресу `http://IP-сервера`):

```nginx
server {
    listen 80 default_server;
    server_name _;
    root /var/www/landing;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

Включите сайт и перезапустите Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/landing /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Откройте в браузере: **http://IP-вашего-сервера** (IP смотрите в панели хостинга или введите `curl ifconfig.me` на сервере).

### Если потом появится домен

Замените в конфиге `server_name _;` на `server_name your-domain.com www.your-domain.com;`. Для HTTPS: `sudo apt install certbot python3-certbot-nginx -y` и `sudo certbot --nginx -d your-domain.com`.

---

## 4. Бот 1 и Бот 2 (systemd)

Чтобы оба бота работали постоянно и перезапускались после сбоя.

### Бот 1

```bash
sudo nano /etc/systemd/system/signal-bot-1.service
```

Подставьте своего пользователя и путь к папке (например `root` и `/root/SignalBot1`):

```ini
[Unit]
Description=Signal Bot 1 (main bot)
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

### Бот 2

```bash
sudo nano /etc/systemd/system/signal-bot-2.service
```

```ini
[Unit]
Description=Signal Bot 2 (signals bot)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/SignalBot2
ExecStart=/root/SignalBot2/venv/bin/python3 main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Включение и запуск

```bash
sudo systemctl daemon-reload
sudo systemctl enable signal-bot-1 signal-bot-2
sudo systemctl start signal-bot-1 signal-bot-2
sudo systemctl status signal-bot-1 signal-bot-2
```

Логи:
- Бот 1: `journalctl -u signal-bot-1 -f`
- Бот 2: `journalctl -u signal-bot-2 -f`

Остановка/перезапуск:
- `sudo systemctl stop signal-bot-1`
- `sudo systemctl restart signal-bot-2`

---

## 5. Порядок настройки

1. Установить Nginx, настроить сайт для лендинга, загрузить файлы в `/var/www/landing`.
2. Настроить домен и при желании HTTPS (certbot).
3. Поднять бота 1: папка, venv, .env, затем systemd для SignalBot1.
4. Поднять бота 2: папка, venv, .env, затем systemd для SignalBot2.
5. Проверить: лендинг открывается в браузере, оба бота отвечают в Telegram.

---

## 6. Кратко

| Задача           | Действие |
|------------------|----------|
| Лендинг          | Nginx, файлы в `/var/www/landing`, конфиг site, при необходимости certbot |
| Бот 1            | `SignalBot1` + venv + .env, юнит `signal-bot-1.service` |
| Бот 2            | `SignalBot2` + venv + .env, юнит `signal-bot-2.service` |

Всё это умещается на одном сервере; боты с лендингом не конфликтуют.
