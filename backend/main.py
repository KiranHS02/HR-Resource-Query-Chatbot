import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models.employee import Employee, EmployeeList
import os
from rag import RAGPipeline

app = FastAPI(title="HR Resource Query Chatbot", description="AI-powered HR assistant for resource allocation queries.")

# CORS setup for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load employee data
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "employees.json")
with open(DATA_PATH, "r") as f:
    employees_data = json.load(f)["employees"]
    employees = [Employee(**emp) for emp in employees_data]

rag_pipeline = RAGPipeline(employees)

@app.get("/employees/search", response_model=List[Employee])
def search_employees(
    skills: Optional[List[str]] = Query(None),
    min_experience: Optional[int] = None,
    availability: Optional[str] = None,
    project: Optional[str] = None
):
    """Search employees by skills, experience, availability, and project."""
    results = employees
    if skills:
        results = [e for e in results if all(skill in e.skills for skill in skills)]
    if min_experience:
        results = [e for e in results if e.experience_years >= min_experience]
    if availability:
        results = [e for e in results if e.availability == availability]
    if project:
        results = [e for e in results if project in e.projects]
    return results

@app.post("/chat")
def chat(query: dict):
    """Chat endpoint for HR resource queries (RAG pipeline integrated)."""
    user_query = query.get("query")
    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required.")
    response = rag_pipeline.query(user_query)
    return {"response": response} 