from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title= "AI Microservice Backend")

app. add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message:str

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend"}

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "user_message": request.message,
        "bot_response": f"You said: {request.message}"
    }