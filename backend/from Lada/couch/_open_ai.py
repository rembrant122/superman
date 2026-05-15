import random
import httpx

from settings import OPENAI_MODEL, OPENAI_API_KEY


async def generate_nouns_from_gpt(count_words: int) -> list[str]:
    url = "https://api.openai.com/v1/chat/completions"

    themes = [
        "природа", "животные", "чувства", "наука", "искусство", "еда",
        "путешествия", "профессии", "спорт", "технологии", "математика", "магия"
        , "предметы быта", "время", "звук", "цвет", "пространство"
    ]
    random.shuffle(themes)
    themes_text = ", ".join(themes[:8])  # случайные 8 тем

    prompt = (
        f"Составь ровно {count_words} простых существительных "
        f"на русском языке в единственном числе, в именительном падеже. "
        f"Подбирай слова по темам: {themes_text}. "
        f"Избегай банальных слов вроде 'кот', 'дом', 'дерево', 'машина', 'река'. "
        f"Ответ дай списком слов, каждое с новой строки, без нумерации и без переводов."
    )

    payload = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 2000,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"].strip()

        words = [w.strip() for w in content.split("\n") if w.strip()]
        return words[:count_words]

    except Exception as e:
        print("Ошибка GPT:", e)
        return []
