import os
from typing import List, Dict, Any
from models.employee import Employee
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import openai
from openai import RateLimitError

# Load embedding model (use a small, fast model for demo)
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# Optionally set OpenAI API key for generation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# --- Retrieval: Embedding + Vector Search ---
def build_employee_index(employees: List[Employee]):
    texts = [f"{e.name} {', '.join(e.skills)} {e.experience_years} years {', '.join(e.projects)} {e.availability}" for e in employees]
    embeddings = model.encode(texts, show_progress_bar=False)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(x=np.array(embeddings).astype('float32'))  # type: ignore
    return index, embeddings, texts

# --- Augmentation: Gather relevant employees ---
def retrieve_employees(query: str, employees: List[Employee], index, embeddings, texts, top_k=3):
    query_emb = model.encode([query])[0]
    D, I = index.search(np.array([query_emb]).astype('float32'), top_k)
    results = [employees[i] for i in I[0]]
    return results

# --- Generation: LLM or template-based ---
def generate_response(query: str, matched: List[Employee]) -> str:
    if OPENAI_API_KEY:
        print("🔑 Using OpenAI LLM for response generation.")
        prompt = (
            f"User query: {query}\n"
            f"Matched employees: {', '.join([e.name for e in matched])}\n"
            f"For each, summarize why they are a good fit."
        )
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an HR assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            print(f"OpenAI RateLimitError: {e}")
            return ("⚠️ Your OpenAI API quota has been exceeded or rate-limited. "
                    "Switching to template-based response.\n\n" +
                    template_response(query, matched))
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return (f"⚠️ OpenAI API error: {e}\nSwitching to template-based response.\n\n" +
                    template_response(query, matched))
    else:
        print("⚡ Using template-based response.")
        return template_response(query, matched)

def template_response(query: str, matched: List[Employee]) -> str:
    if not matched:
        return "Sorry, I couldn't find any suitable employees for your query."
    response = f"Based on your query, I found {len(matched)} candidate(s):\n\n"
    for e in matched:
        response += (
            f"• **{e.name}**\n"
            f"  - Experience: {e.experience_years} years\n"
            f"  - Skills: {', '.join(e.skills)}\n"
            f"  - Projects: {', '.join(e.projects)}\n"
            f"  - Availability: {e.availability}\n\n"
        )
    response += "Would you like more details or to check their availability for meetings?"
    return response

# --- Main RAG pipeline ---
class RAGPipeline:
    def __init__(self, employees: List[Employee]):
        self.employees = employees
        self.index, self.embeddings, self.texts = build_employee_index(employees)

    def query(self, user_query: str, top_k: int = 3) -> str:
        matched = retrieve_employees(user_query, self.employees, self.index, self.embeddings, self.texts, top_k=top_k)
        return generate_response(user_query, matched) 