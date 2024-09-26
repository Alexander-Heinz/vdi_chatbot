import streamlit as st
import time
import uuid
from rag_assistant import answer_question, detect_language
from db_operations import save_conversation, save_feedback, log_interaction


# Set page configuration
st.set_page_config(page_title="VDI-VDE-IT FAQ Chatbot", page_icon="🤖", layout="centered")

# Custom CSS (same as before)
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

# Initialize session state for chat history, conversation IDs, and session ID
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'conversation_ids' not in st.session_state:
    st.session_state['conversation_ids'] = []
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
if 'feedback_given' not in st.session_state:
    st.session_state['feedback_given'] = set()


def display_chat_message(role, content, conversation_id=None):
    with st.container():
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            if role == "user":
                st.image("https://api.dicebear.com/9.x/icons/svg?seed=Liam", width=64)
            else:
                st.image("https://api.dicebear.com/9.x/icons/svg?seed=Maria", width=64)
        
        with col2:
            st.markdown(f"**{role.capitalize()}:** {content}")
        
        if role == "bot" and conversation_id:
            with col3:
                if conversation_id not in st.session_state['feedback_given']:
                    col3.button("👍", key=f"like_{conversation_id}", on_click=lambda: give_feedback(conversation_id, 1))
                    col3.button("👎", key=f"dislike_{conversation_id}", on_click=lambda: give_feedback(conversation_id, -1))
                else:
                    st.write("Feedback given")

def give_feedback(conversation_id, feedback_value):
    save_feedback(conversation_id, feedback_value)
    st.session_state['feedback_given'].add(conversation_id)

st.title("🤖 VDI-VDE-IT Innovationsberatung Chatbot")

st.markdown("""
Willkommen beim FAQ-Chatbot der VDI-VDE Innovation + Technik GmbH. 
Hier können Sie Fragen zu unseren Innovationsberatungsleistungen und Förderprogrammen stellen.

*Sie können Ihre Fragen auch in anderen Sprachen stellen. Der Chatbot erkennt die Sprache automatisch und antwortet entsprechend.*
""")

log_interaction(st.session_state['session_id'], 'page_view')


# Input field for user question
user_question = st.text_input("Stellen Sie hier Ihre Frage:", key="user_input")

# Button to submit question
if st.button("Frage stellen"):
    if user_question:
        # Log question submission
        log_interaction(st.session_state['session_id'], 'question_submitted')
        
        # Add user question to chat history
        st.session_state['chat_history'].append(("user", user_question))
        
        # Display "Thinking..." message
        with st.spinner("Verarbeite Anfrage..."):
            # Get chatbot response
            response = answer_question(user_question)
            time.sleep(1)  # Simulate processing time
        
        # Detect language
        detected_lang = detect_language(user_question)
        
        # Save conversation to database and get conversation ID
        conversation_id = save_conversation(user_question, response, detected_lang, st.session_state['session_id'])
        st.session_state['conversation_ids'].append(conversation_id)
        
        # Add chatbot response to chat history
        st.session_state['chat_history'].append(("bot", response))
        
        # Log response generated
        log_interaction(st.session_state['session_id'], 'response_generated')
    else:
        st.warning("Bitte geben Sie eine Frage ein.")

# Display chat history
st.subheader("Gesprächsverlauf")
for i, (role, content) in enumerate(st.session_state['chat_history']):
    if 'conversation_ids' in st.session_state and len(st.session_state['conversation_ids']) > i // 2:
        conversation_id = st.session_state['conversation_ids'][i // 2] if role == "bot" else None
    else:
        conversation_id = None  # Handle the case where there's no corresponding conversation ID
    
    display_chat_message(role, content, conversation_id)


# Language detection info
if user_question:
    detected_lang = detect_language(user_question)
    lang_names = {
        'de': 'Deutsch',
        'en': 'Englisch',
        'fr': 'Französisch',
        'es': 'Spanisch',
        'it': 'Italienisch'
    }
    lang_name = lang_names.get(detected_lang, detected_lang)
    st.info(f"Erkannte Sprache: {lang_name}")

# Add a clear chat history button
if st.button("Gesprächsverlauf löschen"):
    st.session_state['chat_history'] = []
    st.session_state['conversation_ids'] = []
    st.session_state['feedback_given'] = set()





# Footer
st.markdown("---")
st.markdown("Powered by VDI-VDE Innovation + Technik GmbH")
st.markdown("*Dieser Chatbot verwendet KI-Technologie zur Beantwortung Ihrer Fragen.*")