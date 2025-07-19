import streamlit as st
import requests

st.set_page_config(page_title="HR Resource Query Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 HR Resource Query Chatbot")

# API URL
API_URL = "http://localhost:8000/chat"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message if no chat history
if not st.session_state.messages:
    st.markdown("""
    👋 **Welcome!** I'm your HR Resource Query Assistant. I can help you find the right people for your projects.
    
    **Example queries:**
    - Find Python developers with 3+ years experience
    - Who has worked on healthcare projects?
    - Suggest people for a React Native project
    - Find developers who know both AWS and Docker
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input at the bottom
if prompt := st.chat_input("Type your HR resource query here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Searching for resources..."):
            try:
                response = requests.post(API_URL, json={"query": prompt}, timeout=30)
                response.raise_for_status()
                bot_reply = response.json()["response"]
            except Exception as e:
                bot_reply = f"❌ **Error:** Unable to process your request. Please try again later.\n\nError details: {str(e)}"
        
        message_placeholder.markdown(bot_reply)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Sidebar with additional options
with st.sidebar:
    st.header("💬 Chat Options")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**💡 Tips:**")
    st.markdown("• Be specific about skills and experience")
    st.markdown("• Mention project types or industries")
    st.markdown("• Ask about availability or specific technologies")
    
    st.markdown("---")
    st.markdown("**🔧 API Status:**")
    try:
        # Try to connect to the main API endpoint
        health_check = requests.get(API_URL.replace("/chat", ""), timeout=5)
        if health_check.status_code == 404:
            # 404 is expected for root endpoint, means server is running
            st.success("✅ Backend Connected")
        elif health_check.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.error(f"❌ Backend Error (Status: {health_check.status_code})")
    except requests.exceptions.ConnectionError:
        st.error("❌ Backend Unavailable - Server not running")
    except Exception as e:
        st.error(f"❌ Backend Error: {str(e)}") 