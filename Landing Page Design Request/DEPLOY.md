# Развёртывание лендинга на сервере (по IP)

После сборки лендинг — это папка **`dist`** с статическими файлами. Её нужно отдавать через веб-сервер.

---

## 1. Сборка

```bash
npm install
npm run build
```

В корне проекта появится папка **`dist`** — её и нужно выкладывать на сервер.

---

## 2. Вариант A: Быстрый запуск по IP (Node)

Удобно для проверки в локальной сети или на VPS с Node.

```bash
npm run build
npx serve dist -l 3000 --no-clipboard
```

Сервер слушает на **всех интерфейсах** (в т.ч. по IP). Открой в браузере:

- С этого же компьютера: **http://localhost:3000**
- С телефона/другого устройства в той же сети: **http://IP_СЕРВЕРА:3000**  
  (IP смотри в настройках Wi‑Fi или выполни на сервере `ip addr` / `ifconfig`)

Чтобы слушать на порту 80 (открывать по адресу `http://IP` без порта), нужны права root:

```bash
sudo npx serve dist -l 80 --no-clipboard
```

---

## 3. Вариант B: Просмотр через Vite (после сборки)

```bash
npm run build
npm run preview
```

Сайт будет доступен по **http://IP_СЕРВЕРА:4173** (порт по умолчанию у Vite preview). Запуск с `--host 0.0.0.0` уже прописан в `preview`, поэтому с других устройств по IP зайти можно.

---

## 4. Вариант C: Nginx (рекомендуется для постоянной работы)

Подходит для VPS/сервера с Linux.

### 4.1. Установка Nginx (если ещё нет)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nginx -y
```

### 4.2. Копирование файлов лендинга

Собери проект на своей машине, затем скопируй папку **`dist`** на сервер (через scp, rsync или архив). Пример:

```bash
scp -r dist/* user@IP_СЕРВЕРА:/var/www/landing/
```

На сервере создай каталог при необходимости:
```bash
sudo mkdir -p /var/www/landing
# после копирования файлов:
sudo chown -R www-data:www-data /var/www/landing
```

### 4.3. Конфиг Nginx по IP (без домена)

Создай конфиг:

```bash
sudo nano /etc/nginx/sites-available/landing
```

Вставь (замени `YOUR_SERVER_IP` на реальный IP сервера или используй `_` для приёма по любому адресу):

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name YOUR_SERVER_IP _;
    root /var/www/landing;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Включи сайт и перезапусти Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/landing /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Открой в браузере: **http://IP_СЕРВЕРА** — лендинг должен открываться по IP на любых устройствах.

---

## 5. На одном сервере три проекта (лендинг — один из них)

На одном сервере можно поднять несколько проектов двумя способами: **по разным портам** или **по разным путям** (например `/`, `/bot`, `/landing`). Ниже — оба варианта.

### 5.1. Вариант: три проекта на разных портах

Каждый проект слушает свой порт, Nginx раздаёт их с одного IP.

**Пример раскладки:**

| Проект   | Порт | Как открыть        |
|----------|------|---------------------|
| Проект 1 | 80   | http://IP_СЕРВЕРА   |
| Проект 2 | 3001 | http://IP_СЕРВЕРА:3001 |
| Лендинг | 3002 | http://IP_СЕРВЕРА:3002 |

**Лендинг:** собираешь как обычно (`npm run build`), копируешь `dist` на сервер и поднимаешь, например, так:

```bash
# На сервере (лендинг в /var/www/landing):
npx serve /var/www/landing -l 3002 --no-clipboard
```

Остальные два проекта запускаешь так же на своих портах (80 и 3001). Для постоянной работы лучше оформить сервисы (systemd) или проксировать через Nginx (см. ниже).

**Nginx как единая точка входа (опционально):** можно оставить один порт 80 и раздавать по путям или поддоменам, либо проксировать на разные порты:

```nginx
# В одном server { listen 80; } можно проксировать на разные приложения:
# Лендинг по пути /landing (тогда нужна сборка с base, см. 5.2)
# или лендинг по своему порту через другой server { } блок.
```

Если все три проекта отдаются через Nginx по портам (каждый на своём порту), то для лендинга достаточно одного `server`-блока на порт 3002 с `root /var/www/landing;` и `try_files` как в разделе 4.

---

### 5.2. Вариант: три проекта по разным путям (один порт 80)

Схема вида: **http://IP/** — проект 1, **http://IP/bot/** — проект 2, **http://IP/landing/** — лендинг.

Тогда лендинг должен собираться с **базовым путём** `/landing/`, чтобы корректно подгружались JS/CSS.

**Шаг 1.** В проекте лендинга в `vite.config.ts` задай `base`:

```ts
export default defineConfig({
  base: '/landing/',   // путь, по которому будет открываться лендинг
  // ... остальное без изменений
})
```

**Шаг 2.** Пересобери:

```bash
npm run build
```

**Шаг 3.** На сервере положи содержимое `dist` в каталог, который Nginx отдаёт по пути `/landing/`, например:

```bash
# Файлы лендинга в /var/www/landing/
sudo mkdir -p /var/www/landing
# скопировать сюда содержимое dist
```

**Шаг 4.** В конфиге Nginx для этого сервера добавь location для лендинга (в тот же `server`, где уже есть другие проекты):

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name YOUR_SERVER_IP _;

    # Проект 1 — главная страница (пример)
    location / {
        root /var/www/project1;
        try_files $uri $uri/ /index.html;
    }

    # Проект 2 — по пути /bot/ (пример)
    location /bot {
        alias /var/www/project2/;
        try_files $uri $uri/ /bot/index.html;
    }

    # Лендинг — по пути /landing/
    location /landing {
        alias /var/www/landing/;
        try_files $uri $uri/ /landing/index.html;
    }
}
```

После правок:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Лендинг откроется по адресу: **http://IP_СЕРВЕРА/landing/**.

---

### Кратко по «три проекта на одном сервере»

| Способ              | Лендинг открывать так        | Что сделать с лендингом |
|---------------------|------------------------------|--------------------------|
| Разные порты        | http://IP:3002               | `npm run build`, раздавать `dist` на порту 3002 (serve/nginx) |
| Разные пути         | http://IP/landing/           | В vite задать `base: '/landing/'`, пересобрать, раздавать `dist` из `/landing` в Nginx |

Остальные два проекта настраиваются так же: свой порт или свой `location` и своя папка на диске.

---

## 6. Файрвол

Если сайт не открывается с других устройств:

- **Порт 3000 (serve):** открой порт 3000 (или тот, что указан в `-l`).
- **Порт 80 (nginx):** открой порт 80.
- **Несколько проектов по портам:** открой все используемые порты (80, 3001, 3002 и т.д.).

Пример (ufw на Ubuntu):

```bash
sudo ufw allow 80/tcp
sudo ufw allow 3000/tcp   # если используешь serve на 3000
sudo ufw allow 3001/tcp   # второй проект
sudo ufw allow 3002/tcp   # лендинг
sudo ufw reload
```

---

## Кратко

| Способ              | Команда / действие                          | Открывать по адресу        |
|---------------------|--------------------------------------------|----------------------------|
| Serve (Node)        | `npm run build && npx serve dist -l 3000`  | http://IP:3000             |
| Vite preview        | `npm run build && npm run preview`         | http://IP:4173             |
| Nginx на порту 80   | Разместить `dist` и настроить nginx        | http://IP                  |

Папку **`dist`** можно копировать на любой сервер с веб-сервером (Nginx, Apache, Caddy и т.д.) — лендинг рассчитан на работу по относительным путям и открывается по IP без доп. настроек.

---

## Полная инструкция для повторения (Nginx на сервере)

Ниже — что мы делали и зачем, чтобы ты мог повторить всё без подсказок.

### Что у нас есть

- **Лендинг** — проект на React (Vite). В браузере нужны уже готовые файлы: HTML, JS, CSS.
- **Сервер** — Linux (например Ubuntu) с доступом по SSH. Nginx раздаёт файлы по HTTP.
- **Цель** — открывать сайт по IP (например http://89.169.2.206) с любого устройства, без твоего ПК.

### Общая схема

1. **У себя на компе:** собираем проект → получаем папку **dist** с готовым сайтом.
2. **На сервер:** заливаем **содержимое** dist в папку, которую будет отдавать Nginx.
3. **На сервере:** ставим Nginx, настраиваем конфиг (откуда брать файлы), отключаем дефолтный сайт, включаем наш.
4. **Проверка:** открываем в браузере http://IP_СЕРВЕРА.

Важно: Nginx работает от пользователя **www-data**. Он не имеет права читать каталог **/root/**, поэтому сайт кладём в **/var/www/lending** — туда у www-data есть доступ.

---

### Часть 1. У себя на компьютере

**Что делаем:** собираем лендинг в статические файлы.

```bash
cd "путь/к/проекту/Landing Page Design Request"
npm install
npm run build
```

**Результат:** в проекте появляется папка **dist**. Внутри:
- **index.html** — главная страница;
- **assets/** — папка с .js и .css.

Эти файлы и есть «сайт». Исходники React на сервер не нужны.

---

### Часть 2. Загрузка файлов на сервер

**Что делаем:** копируем на сервер **содержимое** папки dist (не саму папку dist, а то, что внутри).

- Через **scp**, **rsync**, **FileZilla** или архив — как удобно.
- На сервере нужна папка, куда всё положить. Мы использовали **/var/www/lending**.

Если заливаешь в **/root/lending** (или в домашнюю папку), то дальше на сервере мы эти файлы копируем в /var/www/lending — чтобы Nginx (пользователь www-data) мог их читать.

**Структура на сервере должна быть такой:**

```
/var/www/lending/
├── index.html
└── assets/
    ├── index-xxxxx.js
    └── index-xxxxx.css
```

То есть **index.html** и папка **assets** лежат сразу в **/var/www/lending**. Если у тебя сначала получилось так, что внутри lending лежит папка **dist**, а в ней уже index.html и assets — тогда на сервере делаем перенос (команды ниже).

---

### Часть 3. Сервер: установка Nginx

**Что делаем:** ставим веб-сервер Nginx, который будет отдавать файлы по HTTP на порт 80.

```bash
sudo apt update
sudo apt install nginx -y
```

После установки Nginx уже запущен и при заходе по IP показывается стандартная страница «Welcome to nginx!». Мы её потом отключим.

---

### Часть 4. Сервер: папка для сайта и файлы

**Зачем:** Nginx не может читать файлы из /root (нет прав у www-data). Поэтому сайт кладём в /var/www/lending и даём права www-data.

Если файлы уже залиты в **/root/lending** (или в /root/lending/dist):

```bash
sudo mkdir -p /var/www/lending
sudo cp -r /root/lending/* /var/www/lending/
```

Если в /root/lending лежит только папка **dist**, а в ней index.html и assets:

```bash
sudo mv /var/www/lending/dist/* /var/www/lending/
sudo rmdir /var/www/lending/dist
```

Права:

```bash
sudo chown -R www-data:www-data /var/www/lending
```

Проверка:

```bash
ls -la /var/www/lending/
# Должны быть: index.html и папка assets
```

---

### Часть 5. Сервер: конфиг Nginx для лендинга

**Что делаем:** говорим Nginx «на порту 80 отдавай файлы из папки /var/www/lending».

Создаём конфиг сайта:

```bash
sudo nano /etc/nginx/sites-available/landing
```

Вставляем (можно скопировать целиком):

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name _;
    root /var/www/lending;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

**Что значит:**
- **listen 80** — слушать порт 80 (HTTP).
- **server_name _** — принимать запросы по любому имени или IP.
- **root /var/www/lending** — корень сайта: здесь лежат index.html и assets.
- **index index.html** — при запросе «/» отдавать index.html.
- **try_files ... /index.html** — для одностраничного приложения (React): если файл не найден, отдавать index.html (нужно для клиентского роутинга).

Сохранить в nano: **Ctrl+O**, **Enter**, **Ctrl+X**.

---

### Часть 6. Сервер: включить лендинг и отключить дефолтный сайт

**Что делаем:** подключаем наш конфиг к Nginx и отключаем стандартную страницу «Welcome to nginx!».

Включить сайт landing (симлинк в sites-enabled):

```bash
sudo ln -sf /etc/nginx/sites-available/landing /etc/nginx/sites-enabled/
```

Удалить дефолтный сайт, чтобы на порту 80 был только лендинг:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Проверить конфиг и перезагрузить Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

**nginx -t** должен вывести: `syntax is ok` и `test is successful`.

---

### Часть 7. Проверка

На сервере:

```bash
curl -I http://127.0.0.1
```

Ожидается строка **HTTP/1.1 200 OK**.

В браузере открываешь: **http://IP_ТВОЕГО_СЕРВЕРА** (например http://89.169.2.206). Должен открыться лендинг.

---

### Если что-то пошло не так

- **500 Internal Server Error** — чаще всего Nginx не может прочитать файлы. Проверь: `root` в конфиге должен быть `/var/www/lending`, файлы должны быть там, владелец — `www-data` (команда chown выше).
- **Welcome to nginx!** вместо лендинга — не удалён дефолтный сайт: выполни снова `sudo rm -f /etc/nginx/sites-enabled/default` и `sudo systemctl reload nginx`.
- **Сайт не открывается по IP** — проверь файрвол (UFW на сервере: `sudo ufw allow 80/tcp`) и файрвол/сеть у хостера (например Timeweb: в панели открыть входящий порт 80 TCP).

Логи Nginx:
```bash
sudo tail -20 /var/log/nginx/error.log
```

---

### Краткий список команд на сервере (когда файлы уже в /root/lending)

Можно выполнять по порядку (подставь свой путь к файлам, если они лежат не в /root/lending):

```bash
sudo mkdir -p /var/www/lending
sudo cp -r /root/lending/* /var/www/lending/
sudo mv /var/www/lending/dist/* /var/www/lending/ 2>/dev/null; sudo rmdir /var/www/lending/dist 2>/dev/null
sudo chown -R www-data:www-data /var/www/lending
```

Создать конфиг (один раз):
```bash
sudo nano /etc/nginx/sites-available/landing
# вставить блок server { ... } с root /var/www/lending;
```

Включить сайт и перезагрузить Nginx:
```bash
sudo ln -sf /etc/nginx/sites-available/landing /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo sed -i 's|root /root/lending;|root /var/www/lending;|' /etc/nginx/sites-available/landing
sudo nginx -t && sudo systemctl reload nginx
```

После этого сайт доступен по http://IP_СЕРВЕРА.
