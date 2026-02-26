"""Клиент для анализа графика через GPT Vision API."""
import base64
import io
from openai import AsyncOpenAI

from config import OPENAI_API_KEY

# Промпт по ТЗ п.5 — формат ответа пользователю
SYSTEM_PROMPT = """You are a trading chart analyst. The user will send a screenshot of a trading chart.

Analyze the chart and respond in English. Use exactly this format (same headings and structure):

📊 Chart Analysis

Trend: …

Key levels: …

What price is doing now: …

Possible scenarios:
– Scenario 1: …
– Scenario 2: …

Summary: …

If the image is NOT a trading chart, or the chart is too blurry/low quality to read (no visible candles, timeframe, or asset name), respond with exactly this single line and nothing else:
UNREADABLE_CHART"""


async def analyze_chart(image_bytes: bytes) -> str | None:
    """
    Отправляет изображение в GPT Vision и возвращает текстовый анализ.
    Возвращает None при ошибке API.
    Возвращает строку "UNREADABLE_CHART" если график нечитаем.
    """
    if not OPENAI_API_KEY:
        return None

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    mime = "image/jpeg"  # подойдёт и для png в base64

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{image_b64}"},
                        }
                    ],
                },
            ],
            max_tokens=1024,
        )
        text = (response.choices[0].message.content or "").strip()
        return text
    except Exception:
        return None
