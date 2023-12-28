# Example: reuse your existing OpenAI setup
import os
from openai import OpenAI

prompt = """
Answer the following questions as best you can. You have access to the following tools:

DuckDuckGo Results JSON: A wrapper around Duck Duck Go Search. Useful for when you need to answer questions about current events. Input should be a search query. Output is a JSON array of the query results
WebFetcher: Fetch content of a web page
Summarizer: Summarize a web page

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [DuckDuckGo Results JSON, WebFetcher, Summarizer]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin Research how to use the requests library in Python. Use your tools to search and summarize content into a guide on how to use the requests library.
Thought:
"""

# Default using env OPENAI_API_KEY
client = OpenAI(
    #base_url = "http://localhost:1234/v1",
    #api_key = config.openai_key
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo-1106", # this field is currently unused for local LLMs
  #messages=[{"role": "system", "content": "You're a friendly person that tends to encourage others."},
  #          {"role": "user", "content": "How are you?"},
  #          {"role": "assistant", "content": "I'm doing great, thank you! How about you? How can I encourage you today?"},
  #          {"role": "user", "content": "I would like to know the secret of happiness."}])
  messages=[{"role": "user", "content": "Write me a helloworld with Rust."}],
  #messages=[{"role": "user", "content": prompt}],
  #stop=["\nObservation:", "\t\nObservation:"],
  stream=True)

#print(completion.choices[0].message)
for chunk in completion:
    print(chunk.choices[0].delta.content, end="", flush=True)
print("\n")
