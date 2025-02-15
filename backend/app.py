from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Union
from routes import router
from text_preprocessor import Preproccessor
from pydantic import BaseModel

app = FastAPI(
    title="Keyword Preprocessor API",
    description="API for preprocessing keyword strings",
    version="1.0.0"
)
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

app.include_router(router)

class PreprocessResponse(BaseModel):
    processed_keywords: Union[List[str], Dict[str, str]]
    original_input: str
    status: str = "success"

@app.get("/keywords/{keywords}", response_model=PreprocessResponse)
async def preprocess_inputs(request: Request, keywords: str):
    try:
        if not keywords or keywords.isspace():
            return HTTPException(
                status_code=400,
                detail="Keywords string cannot be empty"
            )
            
        preprocessor = Preproccessor()
        processed_result = preprocessor.preprocess(keywords)
        return PreprocessResponse(
            processed_keywords=processed_result,
            original_input=keywords
        )
        
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail=f"Error processing keywords: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)