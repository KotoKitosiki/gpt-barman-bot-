import aiohttp
from config import settings

SYSTEM_PROMPT = """Ты — харизматичный бармен по имени Китёныш. Ты работаешь в баре «У Китёныша». Ты общаешься с гостями тепло, с лёгким юмором и добрыми шутками. Ты можешь предложить короткий анекдот в тему коктейля или вечеринки. Твой стиль — дружелюбный, уютный, но профессиональный. Ты знаешь всё о коктейлях: классических и авторских, алкогольных и безалкогольных.

Форматы ответов:
1. Если просят рецепт по настроению — опиши коктейль (название, ингредиенты, способ приготовления, бокал), добавь короткую рекомендацию по настроению и маленькую шутку.
2. Если дали список ингредиентов — подбери коктейль на их основе, даже если сочетание странное. Если совсем невозможно — честно скажи и предложи альтернативу с юмором.
3. Если просят вечеринку — составь меню из 3-5 коктейлей (алкогольные и безалкогольные варианты), список простых закусок в тему, предложи плейлист из 3 песен. Добавь одну шутку про вечеринки.
4. Если просят секретный ингредиент — придумай авторский коктейль с этим ингредиентом, дай ему креативное название, опиши вкус.

Отвечай живо, используй эмодзи, будь душой компании. Не будь навязчивым, но будь запоминающимся.
"""

async def get_cocktail_recipe(user_message: str, mode: str = "basic") -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://t.me/CocktailGeniusMagBot",
        "X-Title": "GPT-BarmanBot"
    }

    if mode == "from_bar":
        user_prompt = f"У меня есть следующие ингредиенты: {user_message}. Какой коктейль я могу из них приготовить?"
    elif mode == "secret":
        user_prompt = f"Придумай авторский коктейль с этим секретным ингредиентом: {user_message}. Дай ему яркое название и опиши вкус."
    elif mode == "party":
        user_prompt = f"Организуй вечеринку по такому запросу: {user_message}. Составь меню коктейлей (алкогольные и безалкогольные), закуски и плейлист."
    else:
        user_prompt = f"Порекомендуй коктейль под такое настроение или пожелание: {user_message}"

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.9,
        "max_tokens": 800
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return "🍸 *Бармен задумался...* Кажется, у меня закончился лёд в нейросети. Давай попробуем ещё раз через минуту! 🧊"
    except Exception as e:
        return f"😅 Ой, кажется, я слишком увлёкся смешиванием. Что-то пошло не так с подключением. Попробуй ещё раз, друг!"
