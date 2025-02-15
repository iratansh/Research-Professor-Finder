from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from text_preprocessor import Preprocessor 

app = FastAPI()
preprocessor = Preprocessor()

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
        combined_query = " ".join(processed_keywords)

        results = [{"name": "Prof", "score": 0.95, "keywords": []}]
        return {"status": "success", "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)