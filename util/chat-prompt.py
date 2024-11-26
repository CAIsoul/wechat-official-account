from openai import OpenAI 
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read('config.ini')

CHAT_API_KEY = config.get('chatgpt', 'apikey')
KIMI_API_KEY = config.get('kimi', 'apikey')
AI_MODEL = 'moonshot-v1-8k'
# AI_MODEL = 'gpt-4o-mini'

def get_AI_client():
    # client = OpenAI(api_key=CHAT_API_KEY)
    client = OpenAI(
        api_key = KIMI_API_KEY,
        base_url = "https://api.moonshot.cn/v1",
    )
    
    return client

def helloworld():
    client = get_AI_client()
    stream = client.chat.completions.create(
        model=AI_MODEL,
        messages=[{"role": "user", "content": "What do you know about Fuding?"}],
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


async def create_speech():
    client = get_AI_client()
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Sample speech testing."
    )
    response.stream_to_file(speech_file_path)


# asyncio.run(create_speech())
helloworld()