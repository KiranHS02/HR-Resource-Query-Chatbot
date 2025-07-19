# HR Resource Query Chatbot

## Overview
The HR Resource Query Chatbot is an intelligent assistant designed to help HR teams quickly find and recommend employees for projects using natural language queries. It leverages modern retrieval-augmented generation (RAG) techniques, semantic search, and LLMs to provide relevant, human-like recommendations based on a realistic employee dataset.

## Features
- Natural language HR resource search via chat interface
- RAG pipeline: semantic retrieval + augmentation + generation
- Vector similarity search using FAISS and sentence-transformers
- Template-based and LLM-based (Groq api) response generation
- REST API with endpoints for chat and employee search
- Streamlit frontend for interactive chat
- Realistic, diverse employee dataset (50+ entries)
- Modular, extensible codebase

## Architecture
- **Backend:** FastAPI app with RAG pipeline (retrieval, augmentation, generation)
- **Frontend:** Streamlit chat UI
- **Embeddings:** sentence-transformers (MiniLM)
- **Vector Search:** FAISS (in-memory)
- **LLM (optional):** Groq api that uses llama-3.1-8b-instant model
- **Data:** JSON file with employee profiles

**System Flow:**
```
User ──▶ Streamlit UI ──▶ FastAPI /chat ──▶ RAG Pipeline ──▶ Employee Data
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- groq api

### Setup
clone the application

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend (start fronend in different terminal)
```bash
cd frontend
source venv/bin/activate
streamlit run app.py
```

### Configuration
- To use GroqAPI, set `GROQ_API_KEY` in your .env file in backend folder before starting the backend.
- The frontend will connect to the backend at `http://localhost:8000` by default.

## API Documentation

### POST `/chat`
- **Description:** Query the chatbot for employee recommendations.
- **Request:**
  ```json
  { "query": "Find Python developers with 3+ years experience" }
  ```
- **Response:**
  ```json
  { "response": "..." }
  ```

### GET `/employees/search`
- **Description:** Search employees by skills, experience, availability, or project.
- **Query params:** `skills`, `min_experience`, `availability`, `project`
- **Example:** `/employees/search?skills=Python&min_experience=3`
- **Response:**
  ```json
  [ { "id": 1, "name": "Amit Sharma", ... }, ... ]
  ```

## AI Development Process
- **AI Coding Assistants Used:** Cursor AI, GitHub Copilot, ChatGPT
- **How AI Helped:**
  - Code generation for FastAPI, Streamlit, and RAG pipeline
  - Debugging and error resolution
  - Architecture planning and best practices
  - Writing and formatting documentation
- **AI vs Hand-written Code:** ~60% AI-assisted, 40% hand-written (data, edge cases, integration)
- **Interesting AI Solutions:**
  - Modular RAG pipeline with fallback to template
  - Automatic switch to template if LLM quota exceeded
  - Realistic, diverse employee data generation
- **Manual Challenges:**
  - Data realism and diversity
  - Error handling for local-only setup
  - Ensuring clear local setup for reviewers

## Technical Decisions
- **Used Open-source Models:**
  - Open source models are cost effective and free to use 
  - Chose sentence-transformers + FAISS for free, fast, local semantic search
- **Local LLM vs Cloud API:**
  - Cloud Groq API used
- **Performance vs Cost vs Privacy:**
  - Default is local, no-cost, privacy-friendly
  - LLM is opt-in for richer responses

## Future Improvements
- User authentication (HR login)
- Employee profile enrichment (CVs, LinkedIn integration)
- Meeting scheduling and calendar integration
- Feedback/rating system for recommendations
- Local LLM (Ollama, HuggingFace) integration
- Analytics dashboard for HR insights

## Demo
  ![Screenshot](HomePage.png)
  ![Screenshot](Question_Answer.png)

