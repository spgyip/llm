# Example: reuse your existing OpenAI setup
import os
from openai import OpenAI

# openai.api_base = "http://localhost:1234/v1" # point to the local server
# openai.api_key = "" # no need for an API key

client = OpenAI(
    base_url = "http://localhost:1234/v1",
    api_key = "empty-key"
)

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  messages=[{"role": "system", "content": "You're a friendly person that tends to encourage others."},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm doing great, thank you! How about you? How can I encourage you today?"},
            {"role": "user", "content": "I would like to know the secret of happiness."}])

print(completion.choices[0].message)

