from openai import OpenAI
from moment.prompt import prompt


def get_answer(api_key, time):
    client = OpenAI(
        api_key=api_key
    )

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {
              "role": "user",
              "content": prompt.format(time=time)
          }
      ]
    )

    if not completion.choices:
        return ""
    
    return completion.choices[0].message.content