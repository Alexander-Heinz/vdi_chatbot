import streamlit as st
import time
from app import answer_question, detect_language  # Import your chatbot functions

# Set page configuration
st.set_page_config(page_title="VDI-VDE-IT FAQ Chatbot", page_icon="🤖", layout="centered")

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

# Initialize session state for chat history and submit flag
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'submit' not in st.session_state:
    st.session_state['submit'] = False

# Define a callback function to set submit flag to True
def submit_question():
    st.session_state['submit'] = True

def display_chat_message(role, content):
    with st.container():
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if role == "user":
                st.image("https://api.dicebear.com/6.x/initials/svg?seed=JD", width=64)  # User avatar image
            else:
                st.image("https://api.dicebear.com/6.x/bottts/svg?seed=VDI", width=64)  # Bot avatar image
        
        with col2:
            st.markdown(f"**{role.capitalize()}:** {content}")

st.title("🤖 VDI-VDE-IT Innovationsberatung Chatbot")

st.markdown("""
Willkommen beim FAQ-Chatbot der VDI-VDE Innovation + Technik GmbH. 
Hier können Sie Fragen zu unseren Innovationsberatungsleistungen und Förderprogrammen stellen.

*Sie können Ihre Fragen auch in anderen Sprachen stellen. Der Chatbot erkennt die Sprache automatisch und antwortet entsprechend.*
""")

# Input field for user question with on_change set to submit_question callback
user_question = st.text_input("Stellen Sie hier Ihre Frage:", key="user_input", on_change=submit_question)

# Check if the "Frage stellen" button was clicked or if the enter key was pressed
submit_clicked = st.button("Frage stellen")

# Automatically submit question when "Enter" is pressed or button is clicked
if submit_clicked or st.session_state['submit']:
    st.session_state['submit'] = False  # Reset the submit flag after submission
    if user_question:
        # Add user question to chat history
        st.session_state['chat_history'].append(("user", user_question))
        
        # Display "Thinking..." message
        with st.spinner("Verarbeite Anfrage..."):
            # Get chatbot response
            response = answer_question(user_question)
            time.sleep(1)  # Simulate processing time
        
        # Add chatbot response to chat history
        st.session_state['chat_history'].append(("bot", response))
    else:
        st.warning("Bitte geben Sie eine Frage ein.")

# Display chat history
st.subheader("Gesprächsverlauf")
for role, content in st.session_state['chat_history']:
    display_chat_message(role, content)

# Language detection info
if user_question:
    detected_lang = detect_language(user_question)
    lang_names = {
        'de': 'Deutsch',
        'en': 'Englisch',
        'fr': 'Französisch',
        'es': 'Spanisch',
        'it': 'Italienisch'
        # Add more languages as needed
    }
    lang_name = lang_names.get(detected_lang, detected_lang)
    st.info(f"Erkannte Sprache: {lang_name}")

# Add a clear chat history button
if st.button("Gesprächsverlauf löschen"):
    st.session_state['chat_history'] = []
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("Powered by VDI-VDE Innovation + Technik GmbH")
st.markdown("*Dieser Chatbot verwendet KI-Technologie zur Beantwortung Ihrer Fragen.*")
