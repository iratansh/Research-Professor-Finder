from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from text_preprocessor import Preprocessor
from similarity_scoring import ProfessorMatcher
import sys
sys.path.append('backend')
from llm_email import DeepSeekLLM
import threading
from query_IDsearch import ProfessorQuery
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()
preprocessor = Preprocessor()
matcher = ProfessorMatcher()
matcher.load_data()
id_search = ProfessorQuery()
llm = DeepSeekLLM(apiKey="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")
origins = ["http://localhost", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeywordsInput(BaseModel):
    keywords: List[str]

class PrimaryKeyInput(BaseModel):
    primary_key: int

class EmailTipsInput(BaseModel):
    keywords: List[str]
    name: str

@app.post("/match-professors")
async def match_professors(input_data: KeywordsInput):
    try:
        processed_keywords = [preprocessor.preprocess(keyword) for keyword in input_data.keywords]
        results = matcher.get_professors(processed_keywords)
        return {"status": "success", "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/email-tips")
async def email_tips(input_data: EmailTipsInput):
    try:
        logging.info("Received keywords: %s", input_data.keywords)
        processed_keywords = [preprocessor.preprocess(keyword) for keyword in input_data.keywords]
        
        tips = llm.send_message(processed_keywords, input_data.name)
        logging.info("Input name: %s", input_data.name)
        logging.info("Received tips: %s", tips)
        
        return {"status": "success", "tips": tips}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/info")
async def info(input_data: PrimaryKeyInput):
    primary_key = input_data.primary_key
    try:
        event = threading.Event()
        result = {"info": None}

        def fetch_info():
            try:
                result["info"] = id_search.get_professor_by_id(primary_key)
            finally:
                event.set()  
        thread = threading.Thread(target=fetch_info)
        thread.start()
        event.wait()

        return {"status": "success", "info": result["info"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)