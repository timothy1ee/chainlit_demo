import chainlit as cl
import openai
import os

api_key = os.getenv("OPENAI_API_KEY")

endpoint_url = "https://api.openai.com/v1"
client = openai.AsyncClient(api_key=api_key, base_url=endpoint_url)

model_kwargs = {
    "model": "chatgpt-4o-latest",
    "temperature": 0.3,
    "max_tokens": 500
}

@cl.on_message
async def on_message(message: cl.Message):
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": message.content}],
        **model_kwargs
    )

    response_message = cl.Message(content="")
    await response_message.send()
    
    stream = await client.chat.completions.create(messages=[{"role": "user", "content": message.content}], 
                                                  stream=True, **model_kwargs)
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)

    await response_message.update()

    # # https://platform.openai.com/docs/guides/chat-completions/response-format
    # response_content = response.choices[0].message.content

    # await cl.Message(
    #     content=response_content,
    # ).send()