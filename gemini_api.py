import requests

# Function to get response from the Gemini API via OpenRouter
def get_gemini_response(user_message):
    openrouter_api_url = "https://openrouter.ai/api/v1/completions"
    headers = {
        "Authorization": "",  # Replace with your OpenRouter API key
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-chat-experimental-1208",  # Specify the model, e.g., "gemini-chat"
        "prompt": user_message,
        "max_tokens": 100,
        "temperature": 0.7
    }

    # Make a request to the OpenRouter API
    response = requests.post(openrouter_api_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get('choices', [{}])[0].get('text', 'No response from API.')
    else:
        return 'Error connecting to OpenRouter API.'
