# HR Resource Query Chatbot

## Overview
An intelligent HR assistant chatbot that answers resource allocation queries using natural language processing and retrieval-augmented generation (RAG). It helps HR teams find employees by answering queries like:
- "Find Python developers with 3+ years experience"
- "Who has worked on healthcare projects?"
- "Suggest people for a React Native project"
- "Find developers who know both AWS and Docker"

## Features
- RAG pipeline: semantic search + LLM or template-based response
- Vector similarity search (FAISS + sentence-transformers)
- REST API (FastAPI): `/chat` and `/employees/search`
- Streamlit frontend chat interface
- Realistic sample employee dataset
- Modular, industry-standard codebase
- Ready for cloud or local deployment

## Architecture
- **Backend:** FastAPI, RAG pipeline (retrieval, augmentation, generation)
- **Frontend:** Streamlit chat UI
- **Embeddings:** sentence-transformers (MiniLM)
- **Vector Search:** FAISS
- **LLM:** OpenAI GPT-3.5/4 (if API key provided), fallback to template

```
User ──▶ Streamlit UI ──▶ FastAPI /chat ──▶ RAG Pipeline ──▶ Employee Data
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- (Optional) OpenAI API key for advanced LLM responses

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Configuration
- To use OpenAI, set `OPENAI_API_KEY` in your environment.
- To deploy, set `API_URL` in Streamlit secrets or as an environment variable.

## API Documentation

### POST `/chat`
- Request: `{ "query": "Find Python developers with 3+ years experience" }`
- Response: `{ "response": "..." }`

### GET `/employees/search`
- Query params: `skills`, `min_experience`, `availability`, `project`
- Example: `/employees/search?skills=Python&min_experience=3`

## AI Development Process
- **AI Tools Used:** Cursor AI, GitHub Copilot, ChatGPT
- **AI Assistance:** Code generation, debugging, architecture, RAG pipeline, doc writing
- **AI-generated code:** ~80%
- **Manual work:** Data design, edge case handling, deployment scripts
- **Interesting AI solutions:** Modular RAG, fallback to template, Streamlit chat UX
- **Manual challenges:** Data realism, error handling, deployment configs

## Technical Decisions
- **FastAPI:** Async, auto-docs, industry standard
- **Streamlit:** Fast prototyping, easy deployment
- **sentence-transformers + FAISS:** Free, local, fast semantic search
- **OpenAI (optional):** Best-in-class LLM, fallback to template for privacy/cost
- **Deployment:** Docker-ready, cloud-friendly

## Future Improvements
- User authentication (HR login)
- Employee profile enrichment (CVs, LinkedIn)
- Meeting scheduling integration
- Feedback/rating system
- More advanced LLM (Ollama, local models)
- Analytics dashboard

## Demo
  ![Screenshot](demo_screenshot.png)


## Deployment

### Streamlit Cloud (Frontend)
- Push `frontend/` to GitHub
- Go to [Streamlit Cloud](https://streamlit.io/cloud), connect repo, set `API_URL` secret to backend URL

### Render.com (Backend)
- Push `backend/` to GitHub
- Create new FastAPI service on [Render.com](https://render.com/)
