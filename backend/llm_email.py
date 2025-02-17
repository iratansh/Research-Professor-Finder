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
            "messages": [{"role": "user", "content": f"Give me a few tips to email a professor at the University of Alberta with these interests: {interests}"}]
        }
        response = requests.post(self.apiURL, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Request failed with status code {response.status_code}")
        
if __name__ == "__main__":
    llm = DeepSeekLLM("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")
    response = llm.send_message("machine learning")
    print(response)