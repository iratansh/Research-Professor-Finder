import fastapi
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from text_preprocessor import Preproccessor
from fastapi.responses import JSONResponse

app = fastapi.FastAPI()

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

@app.get("/keywords/{keywords}")
def preprocess_inputs(request, keywords: str):
    preprocessor = Preproccessor()
    return JSONResponse(content=preprocessor.preprocess(keywords))