from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate feedback from OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a senior code reviewer."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
    max_tokens=500
)

feedback = response.choices[0].message.content
