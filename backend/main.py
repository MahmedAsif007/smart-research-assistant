#main.py
import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
 
from graph import graph, rag, csv_manager
 
load_dotenv()
 
app = FastAPI(title="Smart Research & Data Assistant")
 
# Allow Angular frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.app\.github\.dev",
    # allow_origins=["*"],
    # allow_origins=["https://redesigned-chainsaw-wr64qv74qp9cvx9-4200.app.github.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
class ChatRequest(BaseModel):
    message: str
 
 
@app.get("/")
def root():
    return {"message": "Smart Research & Data Assistant is running"}
 
 
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": os.getenv("OLLAMA_MODEL", "not set")
    }
 
 
@app.post("/upload/document")
async def upload_document(file: UploadFile = File(...)):
    suffix = ".pdf" if file.filename.lower().endswith(".pdf") else ".txt"
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
 
    file_type = "pdf" if suffix == ".pdf" else "txt"
    rag.add_documents(tmp_path, file_type)
    os.unlink(tmp_path)
 
    return {"message": f"Document '{file.filename}' uploaded successfully"}
 
 
@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    info = csv_manager.load_csv(content, file.filename)
    return {
        "message": f"CSV '{file.filename}' loaded successfully",
        "info": info
    }
 
 
@app.post("/chat")
async def chat(req: ChatRequest):
    result = graph.invoke({
        "query": req.message,
        "messages": [],
        "rag_context": "",
        "csv_context": "",
        "final_answer": ""
    })
 
    return {
        "answer": result.get("final_answer", "No answer generated"),
        "rag_used": bool(result.get("rag_context")),
        "csv_used": bool(result.get("csv_context"))
    }