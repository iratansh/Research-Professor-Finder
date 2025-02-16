from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from text_preprocessor import Preprocessor
from selection_query import ProfessorSearch
from LLMemail import DeepSeekLLM
import threading

app = FastAPI()
preprocessor = Preprocessor()
professor_search = ProfessorSearch()
llm = DeepSeekLLM(apiKey="")

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

@app.post("/match-professors")
async def match_professors(input_data: KeywordsInput):
    try:
        processed_keywords = [preprocessor.preprocess(keyword) for keyword in input_data.keywords]
        # professors = professor_search.search(processed_keywords) uncommented for when database is finished

        # pass the professors to ranking model (what should be passed is their keywords or bios)
        # create a new dict with the professors in ranked order and return for frontend
        

        results = [{"name": "Prof", "score": 0.95, "keywords": processed_keywords}]
        return {"status": "success", "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/email-tips")
async def email_tips(input_data: KeywordsInput):
    try:
        processed_keywords = [preprocessor.preprocess(keyword) for keyword in input_data.keywords]
        
        result = {"tips": None}
        event = threading.Event()

        def fetch_tips():
            try:
                result["tips"] = llm.send_message(processed_keywords)
            finally:
                event.set()  
        thread = threading.Thread(target=fetch_tips)
        thread.start()
        event.wait()

        return {"status": "success", "tips": result["tips"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)