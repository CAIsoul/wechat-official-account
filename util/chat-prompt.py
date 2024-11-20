from openai import OpenAI
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config.get('chatgpt', 'apikey')

client = OpenAI(api_key=API_KEY)

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What do you know about Fuding?"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
