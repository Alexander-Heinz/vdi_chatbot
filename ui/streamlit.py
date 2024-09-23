import streamlit as st
import time
# from faq_chatbot import answer_question  # Import your chatbot function


### CHATBOT FUNCTIONS
from elasticsearch import Elasticsearch, helpers

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")




# Set page configuration
st.set_page_config(page_title="Multilingual FAQ Chatbot", page_icon="🤖", layout="centered")

# Custom CSS to improve the UI
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 18px;
    }
    .stButton > button {
        font-size: 18px;
        font-weight: bold;
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
    .chat-message .avatar {
      width: 20%;
    }
    .chat-message .avatar img {
      max-width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
    }
    .chat-message .message {
      width: 80%;
      padding: 0 1.5rem;
      color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def display_chat_message(role, content):
    with st.container():
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if role == "user":
                st.image("https://api.dicebear.com/6.x/initials/svg?seed=JD", width=64)
            else:
                st.image("https://api.dicebear.com/6.x/bottts/svg?seed=Bob", width=64)
        
        with col2:
            st.markdown(f"**{role.capitalize()}:** {content}")

st.title("🤖 Multilingual FAQ Chatbot")

st.markdown("""
This chatbot can answer your questions in multiple languages. 
It will automatically detect the language you're using and respond accordingly.
""")

# Input field for user question
user_question = st.text_input("Ask your question here:", key="user_input")

# Button to submit question
if st.button("Ask"):
    if user_question:
        # Add user question to chat history
        st.session_state['chat_history'].append(("user", user_question))
        
        # Display "Thinking..." message
        with st.spinner("Thinking..."):
            # Get chatbot response
            response = answer_question(user_question)
            time.sleep(1)  # Simulate processing time
        
        # Add chatbot response to chat history
        st.session_state['chat_history'].append(("bot", response))
    else:
        st.warning("Please enter a question.")

# Display chat history
st.subheader("Chat History")
for role, content in st.session_state['chat_history']:
    display_chat_message(role, content)

# Language detection info
if user_question:
    detected_lang = detect_language(user_question)
    st.info(f"Detected language: {detected_lang}")

# Add a clear chat history button
if st.button("Clear Chat History"):
    st.session_state['chat_history'] = []
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("Powered by OpenAI GPT and Elasticsearch")