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
                    "content": f"Generate a professional email template based on the following details:{interests}.The response should include only the email template with no additional commentary, explanations, or conversational elements. Begin directly with the email content and do not include any preamble or closing remarks outside of the email itself.",
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
