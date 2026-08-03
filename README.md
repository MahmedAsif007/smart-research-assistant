# smart-research-assistant
Assistance chat bot that works on given data

Smart Research & Data Assistant
Overview

Smart Research & Data Assistant is an AI-powered application that enables users to:

Chat with an AI assistant
Upload PDF/TXT documents and ask questions
Upload CSV datasets and perform analysis
Use Retrieval-Augmented Generation (RAG) for document intelligence
Maintain conversational memory
Utilize a multi-agent architecture powered by LangGraph

The system combines:

Angular 21 Frontend
FastAPI Backend
LangGraph Multi-Agent Workflow
Chroma Vector Database
HuggingFace Embeddings
Ollama-hosted LLMs

Features
Chat Assistant
Natural language conversations
Multi-turn conversation support
Context-aware responses
Conversational memory
Document Intelligence
Upload PDF files
Upload TXT files
Chunking and embedding generation
Semantic search using vector similarity
RAG-powered question answering
CSV Intelligence
Upload CSV datasets
Dataset summarization
Metadata extraction
Question answering based on uploaded data
Multi-Agent Workflow
Research Agent
Data Analyst Agent
Critic Agent
Synthesizer Agent


Technology Stack
Frontend
Angular 21
TypeScript
SCSS
Angular Signals
Standalone Components
Backend
FastAPI
LangGraph
LangChain
ChromaDB
HuggingFace Embeddings
Ollama
AI Models

LLM Model : gpt-oss:20b
Embedding Model : sentence-transformers/all-MiniLM-L6-v2

Frontend Architecture
Angular
│
├── Layout
│    └── Main Layout
│
├── Shared Components
│    └── Button
│
├── Core Services
│    └── ApiService
│
└── Features
     └── Chat


Frontend Flow
Application Startup
Angular Application
        │
        ▼
Load Main Layout
        │
        ▼
Call /health
        │
        ▼
Display Backend Status


Chat Flow
User Message
        │
        ▼
sendMessage()
        │
        ▼
POST /chat
        │
        ▼
Backend Processing
        │
        ▼
Response Returned
        │
        ▼
Display Assistant Message

PDF Upload Flow
Select PDF
        │
        ▼
Upload Document API
        │
        ▼
Backend Processing
        │
        ▼
Document Embedded
        │
        ▼
Stored In Vector Database


Backend Architecture
FastAPI
│
├── Main API Layer
│
├── LangGraph
│
├── RAG Engine
│
├── CSV Manager
│
├── Embedding Service
│
└── ChromaDB


Backend Flow
Chat Request
POST /chat
        │
        ▼
Graph Invocation
        │
        ▼
Research Agent
        │
        ▼
Data Analyst Agent
        │
        ▼
Critic Agent
        │
        ▼
Synthesizer Agent
        │
        ▼
Final Response


Multi-Agent Workflow

The application follows a sequential multi-agent execution model.

Research Agent
Responsibility

Retrieve relevant information from uploaded documents.

Process
User Question
        │
        ▼
Vector Search
        │
        ▼
Retrieve Similar Chunks
        │
        ▼
Return Document Context


Data Analyst Agent
Responsibility

Analyze uploaded CSV datasets.

Process
CSV Dataset
        │
        ▼
Metadata Extraction
        │
        ▼
Dataset Summary
        │
        ▼
Return CSV Context


Critic Agent
Responsibility

Review gathered information.

Process
Document Context
        +
CSV Context
        │
        ▼
Critical Review
        │
        ▼
Identify Missing Information



RAG Workflow
PDF/TXT Upload
        │
        ▼
Document Loader
        │
        ▼
Text Splitter
        │
        ▼
Chunk Creation
        │
        ▼
MiniLM Embeddings
        │
        ▼
Chroma Vector Database



Retrieval Process
User Question
        │
        ▼
Question Embedding
        │
        ▼
Similarity Search
        │
        ▼
Relevant Chunks
        │
        ▼
LLM Response



Conversation Memory Flow
User Message
        │
        ▼
Conversation History
        │
        ▼
Stored In Memory
        │
        ▼
Passed To Synthesizer
        │
        ▼
Context-Aware Response



API Endpoints
Health Check
GET /health
{
  "status": "ok",
  "model": "gpt-oss:20b"
}

Chat
POST /chat
{ request
  "message": "What is Angular?"
}

{ response
  "answer": "Angular is..."
}


Upload document
POST /upload/document
supported document
PDF, TXT, CSV


Run backend
cd backend

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run front end
cd frontend

npm install

npm start or ng serve --host 0.0.0.0 --port 4200



Future Enhancements
Phase 2
Session-based conversations
Persistent chat history
Multiple chat sessions
Streaming responses
Source citation display
Upload progress indicators
Dark mode
User authentication
