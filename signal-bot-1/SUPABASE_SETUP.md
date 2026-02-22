# Настройка Supabase для двух ботов

Оба бота (основной и второй — только рассылка) используют **одну базу данных** в Supabase.

---

## 1. Что такое Supabase и что нужно

- **Supabase** — облачная база данных (PostgreSQL) + API. Замена своей установки PostgreSQL.
- Нужно: **аккаунт** (бесплатный тариф есть), **один проект**, **строка подключения** к БД.

---

## 2. Регистрация и создание проекта

1. Зайдите на [supabase.com](https://supabase.com) и нажмите **Start your project**.
2. Войдите через GitHub или email.
3. **New project**:
   - **Name** — например `signal-bots`
   - **Database Password** — придумайте и **сохраните** (нужна для строки подключения).
   - **Region** — ближайший к вам.
4. Нажмите **Create new project** и дождитесь создания (1–2 минуты).

---

## 3. Где взять данные для ботов

В проекте откройте **Settings** (иконка шестерёнки) → **Database**.

- **Connection string** → **URI**  
  Будет строка вида:
  ```text
  postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
  ```
  Подставьте вместо `[YOUR-PASSWORD]` пароль, который задали при создании проекта.  
  Эту строку используйте как **`DATABASE_URL`** в `.env` **обоих ботов**.

Для **прямого подключения** (порт 5432) в том же разделе есть **Direct connection** — можно использовать и его.

---

## 4. Создание таблиц в Supabase

В левом меню: **SQL Editor** → **New query**. Вставьте скрипт ниже и нажмите **Run**.

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

-- Индексы для быстрого поиска
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_users_is_premium_active ON users(is_premium, is_active);
CREATE INDEX IF NOT EXISTS idx_users_split_group ON users(split_group);
CREATE INDEX IF NOT EXISTS idx_admins_telegram_id ON admins(telegram_id);
```

После выполнения таблицы появятся в **Table Editor**.

---

## 5. Добавление первого админа

В **SQL Editor** выполните (подставьте свой Telegram ID вместо `123456789`):

```sql
INSERT INTO admins (telegram_id)
VALUES (123456789)
ON CONFLICT (telegram_id) DO NOTHING;
```

Узнать свой ID можно у [@userinfobot](https://t.me/userinfobot) в Telegram.

---

## 6. Переменные окружения для ботов

В **.env** каждого бота укажите общую БД:

```env
# Общая база Supabase для обоих ботов
DATABASE_URL=postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

- Для **основного бота** остаётся его `BOT_TOKEN`, платежи, меню и т.д.
- Для **второго бота** — другой `BOT_TOKEN` (второй бот от BotFather), тот же `DATABASE_URL` и те же `ADMIN_IDS`.

Оба бота подключаются к одной и той же базе: одни и те же `users`, `admins`, `signals`, `payments`.

---

## 7. Краткий чек-лист

| Шаг | Действие |
|-----|----------|
| 1 | Зарегистрироваться на supabase.com |
| 2 | Создать проект, сохранить пароль БД |
| 3 | Settings → Database → скопировать Connection string (URI), подставить пароль → это `DATABASE_URL` |
| 4 | SQL Editor → выполнить скрипт создания таблиц |
| 5 | SQL Editor → вставить своего админа в `admins` |
| 6 | В .env обоих ботов прописать один и тот же `DATABASE_URL` |

Готово. Дальше запускаете первый и второй бот — они оба работают с одной базой Supabase.
