from openai import OpenAI
import json

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

available_functions = {
    "get_current_weather": get_current_weather,
}

def run_conversation(client):
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        }
    ]
    tool_choice = {
        "type": "function",
        "function": {
            "name": "get_current_weather"
        }
    }
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        tools=tools,
        tool_choice=tool_choice
    )
    response_message = completion.choices[0].message
    
    fn_name = response_message.tool_calls[0].function.name
    fn = available_functions[fn_name]
    fn_args = json.loads(response_message.tool_calls[0].function.arguments)
    fn_response = fn(
        location=fn_args.get("location"),
        unit=fn_args.get("unit"),
    )
    
    #messages.append(fn_response)
    messages.append(
        {
            "role": "function",
            "name": fn_name,
            "content": fn_response,
        }
    )
 
    print(messages)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    ) 
    return completion.choices[0].message

# Default using env OPENAI_API_KEY
client = OpenAI(
    #base_url = "http://localhost:1234/v1",
    #api_key = config.openai_key
)
print(run_conversation(client))
