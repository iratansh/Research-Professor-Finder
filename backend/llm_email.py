import requests


class DeepSeekLLM:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.apiURL = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.apiKey}",
            "Content-Type": "application/json",
        }

    def send_message(self, interests):
        data = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Only respond with the email template, nothing else. Keep these interests in mind when writing the email. Make sure it is easily copyable, and not in markdown or thats not easily copyable into gmail: {interests}",
                }
            ],
        }
        response = requests.post(self.apiURL, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    llm = DeepSeekLLM("")
    response = llm.send_message("machine learning")
    print(response)
