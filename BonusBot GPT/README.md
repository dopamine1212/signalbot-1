# Chart Analysis Telegram Bot (aiogram)

Бот принимает скриншоты торговых графиков и возвращает текстовый анализ через GPT Vision: тренд, ключевые уровни и сценарии.

## Стек

- **Python 3.10+**
- **aiogram 3** — Telegram Bot API
- **OpenAI API** — GPT-4o Vision для анализа изображений

## Установка

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Настройка

1. Скопируйте `.env.example` в `.env`:
   ```bash
   cp .env.example .env
   ```
2. В `.env` укажите:
   - `TELEGRAM_BOT_TOKEN` — токен от [@BotFather](https://t.me/BotFather)
   - `OPENAI_API_KEY` — ключ OpenAI API

## Запуск

Перейдите в папку `bonus bot` и запустите бота:

```bash
cd "bonus bot"
python bot.py
```

## Поведение по ТЗ

1. **Старт** — приветствие и предложение отправить скриншот графика.
2. **Ввод** — принимаются фото и файлы PNG/JPG.
3. **Не изображение** — ответ: «Please send a screenshot of a trading chart».
4. **Получение изображения** — сразу ответ «Chart received. Analyzing…».
5. **Анализ** — отправка в GPT Vision, ответ в формате: Trend, Key levels, What price is doing now, Possible scenarios, Summary.
6. **Плохое качество** — если график нечитаем: просьба отправить более чёткий скрин с названием актива, таймфреймом и видимыми свечами.
7. **После ответа** — «You can send another chart whenever you're ready».
8. **Ошибка API** — «Something went wrong while analyzing the chart. Please try again in a moment.»
