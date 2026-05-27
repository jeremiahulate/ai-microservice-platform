import os
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Message, Document

Base.metadata.create_all(bind=engine)

app = FastAPI(title= "AI Microservice Backend")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend"}

@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    bot_response = f"You said: {request.message}"

    message = Message(
        user_message=request.message,
        bot_response=bot_response
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "id": message.id,
        "user_message": message.user_message,
        "bot_response": message.bot_response,
        "created_at": message.created_at
    }

@app.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.created_at.desc()).all()

    return [
        {
            "id": msg.id,
            "user_message": msg.user_message,
            "bot_response": msg.bot_response,
            "created_at": msg.created_at
        }
        for msg in messages
    ]

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported for now.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)
    
    document = Document(
        filename=file.filename,
        file_path=file_path,
        content_type=file.content_type,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "id": document.id,
        "filename": document.filename,
        "file_path": document.file_path,
        "content_type": document.content_type,
        "created_at": document.created_at,
    }

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.created_at.desc()).all()

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_path": doc.file_path,
            "content_type": doc.content_type,
            "created_at": doc.created_at,
        }
        for doc in documents
    ]