import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

async def stream_response(prompt: str, model="gpt-3.5-turbo"):
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    async for chunk in response:
        delta = chunk.choices[0].delta.get("content", "")
        yield delta
