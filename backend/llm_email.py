import requests
import concurrent.futures
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

class DeepSeekLLM:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        if not apiKey:
            raise ValueError("API key is required")
        self.apiURL = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.apiKey}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:5173/",  
            "X-Title": "LocalDev"  
        }
        
        self.session = requests.Session()
        retry_strategy = Retry(
            total=2, 
            backoff_factor=0.5,  
            status_forcelist=[429, 500, 502, 503, 504] 
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        
    def send_message(self, interests, name, timeout=30):
        data = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Draft an email template to a University of Alberta professor with this name {name} and with the following interests: {interests}, asking if they have any open research positions.The response should include only the email template with no additional commentary, explanations, or conversational elements. Begin directly with the email content and do not include any preamble or closing remarks outside of the email itself. You are sending an email for the first time, so things like introductions etc are very important. You can assume that I attend the University of Alberta.",
                }
            ],
            "temperature": 0.7, 
            "max_tokens": 800,   
            "stream": False, 
            "top_p": 0.95    
        }
        
        try:
            response = self.session.post(
                self.apiURL, 
                headers=self.headers, 
                json=data,
                timeout=timeout  
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception("Request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    async def send_message_async(self, interests):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.send_message, interests)
            try:
                return future.result(timeout=30)
            except concurrent.futures.TimeoutError:
                raise Exception("Request timed out")

if __name__ == "__main__":
    llm = DeepSeekLLM("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")

    try:
        start_time = time.time()
        response = llm.send_message("machine learning", timeout=20)
        print(f"Response received in {time.time() - start_time:.2f} seconds")
        print(response)
    except Exception as e:
        print(f"Error: {str(e)}")