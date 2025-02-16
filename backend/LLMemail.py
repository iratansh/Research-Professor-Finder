import requests

class DeepSeekLLM:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.apiURL = 'https://openrouter.ai/api/v1/chat/completions'
        self.headers = {
            'Authorization': f'Bearer {self.apiKey}',
            'Content-Type': 'application/json'
        }
    def send_message(self, interests):
        data = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [{"role": "user", "content": f"Give me a few tips to email a professor with these interests, if there are any names included in the interests, just disregard them: {interests}"}]
        }
        response = requests.post(self.apiURL, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Request failed with status code {response.status_code}")