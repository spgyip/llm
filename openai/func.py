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

def run_conversation(client):
    # 在這邊我們提供functions這個data給OpenAI，告訴OpenAI我們的function interface
    # 以及他需要的參數等等
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
    
    # 這邊user已經很明確的說要Boston的天氣，所以OpenAI會回傳  
    # {"location": "Boston"}
    # 到這邊為止，OpenAI根據我們給的function interface，從user prompt中擷取需要的資訊
    # 變成function call的形式回傳回來（見下面的response_message）
    response_message = completion.choices[0].message
    print(response_message)
    exit(1)

    
    # 這裡是我們上面想要被操作的function，把它放進dict接下來要提供給OpenAI
    available_functions = {
        "get_current_weather": get_current_weather,
    }
    function_name = response_message.function_call.name
    function_to_call = available_functions[function_name]
    # 這邊用前一段回傳的response_message中的function_call拿出需要的資訊，傳到我們真正的function中
    # get_current_weather(location="Boston, MA")
    # 拿到上面function中已經寫的dummy json
    function_args = json.loads(response_message["function_call"]["arguments"])
    function_response = function_to_call(
        location=function_args.get("location"),
        unit=function_args.get("unit"),
    )
    
    # 前面提過的要把前面的訊息append上去，OpenAI才知道自己講過什麼
    messages.append(response_message)
    # 將真正的function的回傳json傳給OpenAI  
    messages.append(
        {
            "role": "function",
            "name": function_name,
            "content": function_response,
        }
    )
    # 最後OpenAI將本來是json格式的值，根據我們給的function metadata變成人看得懂的話
    # 見下面的second_response
    second_response = client.chat.completion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    ) 
    return second_response

client = OpenAI(
    base_url = "http://localhost:1234/v1",
    api_key = "empty-key"
)
print(run_conversation(client))
