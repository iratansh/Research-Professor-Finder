from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from text_preprocessor import Preproccessor

app = FastAPI()

keywords_array = []

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class KeywordsInput(BaseModel):
    keywords: List[str]

@app.post("/keywords")
async def store_keywords(input_data: KeywordsInput):
    try:
        keywords_array.extend(input_data.keywords)
        preprocessor = Preproccessor()
        keywords_array = [preprocessor.preprocess(keyword) for keyword in keywords_array]
        return {"status": "success", "stored_keywords": keywords_array}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error storing keywords: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)