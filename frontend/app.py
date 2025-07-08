import streamlit as st
import requests

st.set_page_config(page_title="HR Resource Query Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 HR Resource Query Chatbot")

API_URL = st.secrets["API_URL"] if "API_URL" in st.secrets else "http://localhost:8000/chat"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown("""
Type your HR resource query below. Example queries:
- Find Python developers with 3+ years experience
- Who has worked on healthcare projects?
- Suggest people for a React Native project
- Find developers who know both AWS and Docker
""")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your query:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, json={"query": user_input}, timeout=30)
            response.raise_for_status()
            bot_reply = response.json()["response"]
        except Exception as e:
            bot_reply = f"Error: {e}"
    st.session_state["messages"].append({"role": "bot", "content": bot_reply})

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"<div style='text-align:right'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left'><b>Bot:</b> {msg['content']}</div>", unsafe_allow_html=True) 