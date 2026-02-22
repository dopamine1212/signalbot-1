# Пошаговое подключение PostgreSQL через Supabase

Один раз настраиваете Supabase — оба бота (signal-bot-1 и signal-bot-2) работают с одной базой.

---

## Шаг 1. Регистрация на Supabase

1. Откройте в браузере: **https://supabase.com**
2. Нажмите **Start your project**
3. Войдите через **GitHub** или **Email** (зарегистрируйтесь, если нет аккаунта)

---

## Шаг 2. Создание проекта

1. После входа нажмите **New project**
2. Заполните:
   - **Name** — например `signal-bots` (любое имя)
   - **Database Password** — придумайте надёжный пароль и **обязательно сохраните** (запишите в блокнот). Он понадобится для строки подключения.
   - **Region** — выберите ближайший регион (например, Frankfurt или Stockholm для Европы)
3. Нажмите **Create new project**
4. Подождите 1–2 минуты, пока проект создаётся (зелёная галочка)

---

## Шаг 3. Получить строку подключения (Connection string)

1. В левом боковом меню Supabase нажмите **Settings** (иконка шестерёнки внизу)
2. В открывшемся меню выберите **Database**
3. Прокрутите страницу вниз до блока **Connection string**
4. Переключитесь на вкладку **URI**
5. Увидите строку вида:
   ```text
   postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
   В интерфейсе Supabase уже подставлены `[PROJECT-REF]` и `[REGION]`, но **пароль скрыт**.

6. **Важно:** используйте строку с **Connection pooling** (пулер), а не Direct:
   - Под блоком Connection string бывают вкладки или режимы: **Session** (Direct) и **Transaction** (Pooler).
   - Берите строку, где хост заканчивается на **`.pooler.supabase.com`** и порт **`6543`**.
   - Не берите хост `db.xxxxx.supabase.co` с портом `5432` — с него часто бывает "No route to host".
7. Нажмите **Copy** и вставьте строку в блокнот. Найдите **`[YOUR-PASSWORD]`** и замените на пароль из Шага 2.
8. В строке не должно остаться `[ ]`. Пример правильной строки:
   ```text
   postgresql://postgres.abcdefghijklmn:MySecretPass123@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
   ```
9. Эта строка — ваша **DATABASE_URL** для обоих ботов.

---

## Шаг 4. Создать таблицы в базе

1. В левом меню Supabase нажмите **SQL Editor** (иконка с символом `</>`)
2. Нажмите **New query**
3. Скопируйте **весь** код ниже и вставьте в окно запроса:

```sql
-- Пользователи (общая таблица для обоих ботов)
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    is_active INTEGER DEFAULT 1,
    is_premium INTEGER DEFAULT 0,
    balance DOUBLE PRECISION DEFAULT 0.0,
    split_group INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Платежи
CREATE TABLE IF NOT EXISTS payments (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    amount DOUBLE PRECISION NOT NULL,
    currency TEXT DEFAULT 'USD',
    crypto_currency TEXT,
    status TEXT DEFAULT 'pending',
    transaction_hash TEXT,
    payment_id TEXT UNIQUE,
    payment_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Сигналы
CREATE TABLE IF NOT EXISTS signals (
    id BIGSERIAL PRIMARY KEY,
    text TEXT,
    photo_ids TEXT,
    is_active INTEGER DEFAULT 1,
    split_group INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by BIGINT
);

-- Админы (одни и те же для обоих ботов)
CREATE TABLE IF NOT EXISTS admins (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    added_at TIMESTAMPTZ DEFAULT NOW(),
    added_by BIGINT
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_is_premium_active ON users(is_premium, is_active);
CREATE INDEX IF NOT EXISTS idx_users_split_group ON users(split_group);
CREATE INDEX IF NOT EXISTS idx_admins_telegram_id ON admins(telegram_id);
```

4. Нажмите **Run** (или Ctrl+Enter / Cmd+Enter)
5. Внизу должно появиться сообщение об успешном выполнении. Таблицы появятся в **Table Editor** в левом меню.

---

## Шаг 5. Добавить себя как админа

1. Оставьте открытым **SQL Editor** (или снова откройте **New query**)
2. Узнайте свой Telegram ID: напишите боту [@userinfobot](https://t.me/userinfobot) в Telegram — он пришлёт ваш ID (число, например `123456789`)
3. В SQL Editor выполните (подставьте **свой** ID вместо `123456789`):

```sql
INSERT INTO admins (telegram_id)
VALUES (123456789)
ON CONFLICT (telegram_id) DO NOTHING;
```

4. Нажмите **Run**

---

## Шаг 6. Прописать DATABASE_URL в первом боте (signal-bot-1)

1. Откройте в редакторе файл: **signal-bot-1/.env**
2. Найдите строку **DATABASE_URL** (или добавьте её, если нет)
3. Вставьте туда **ту самую** строку из Шага 3 (с подставленным паролем), без кавычек, одной строкой:

```env
DATABASE_URL=postgresql://postgres.xxxxx:ваш_пароль@aws-0-регион.pooler.supabase.com:6543/postgres
```

4. Сохраните файл

---

## Шаг 7. Прописать DATABASE_URL во втором боте (signal-bot-2)

1. Откройте файл: **signal-bot-2/.env**
2. Найдите **DATABASE_URL** (или добавьте)
3. Вставьте **ту же самую** строку, что и в signal-bot-1 (один и тот же Supabase):

```env
DATABASE_URL=postgresql://postgres.xxxxx:ваш_пароль@aws-0-регион.pooler.supabase.com:6543/postgres
```

4. Сохраните файл

---

## Шаг 8. Проверка

1. Запустите первый бот:
   - В терминале перейдите в папку проекта, затем: `cd signal-bot-1`
   - Выполните: `python3 main.py`
   - Не должно быть ошибок про DATABASE_URL или подключение к БД

2. Запустите второй бот в **другом** терминале:
   - `cd signal-bot-2` (из папки проекта)
   - `python3 main.py`
   - То же — без ошибок подключения

Если оба бота запустились — PostgreSQL через Supabase подключён, оба используют одну базу.

---

## Краткий чек-лист

| № | Действие |
|---|----------|
| 1 | Зарегистрироваться на supabase.com |
| 2 | New project → имя, пароль (сохранить!), регион → Create |
| 3 | Settings → Database → Connection string → URI → Copy → заменить [YOUR-PASSWORD] на свой пароль |
| 4 | SQL Editor → New query → вставить скрипт таблиц → Run |
| 5 | SQL Editor → INSERT в admins свой Telegram ID → Run |
| 6 | В signal-bot-1/.env прописать DATABASE_URL (строка из шага 3) |
| 7 | В signal-bot-2/.env прописать тот же DATABASE_URL |
| 8 | Запустить оба бота и проверить, что нет ошибок подключения |

Готово.
