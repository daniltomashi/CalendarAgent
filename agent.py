from openai import OpenAI
from configparser import ConfigParser


config = ConfigParser()
config.read('creds/config.ini')

openai_key = config["KEYS"]["openai_key"]



def answer(prompt):
    client = OpenAI(api_key=openai_key)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ]
    )


    return ...