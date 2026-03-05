import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Page Configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    :root {
        --primary-color: #1E3A5F;
        --secondary-color: #2E5077;
        --accent-color: #3CAEA3;
        --background-color: #F5F7FA;
        --card-bg: #FFFFFF;
        --border-color: #E0E4E8;
    }
    .stApp { background-color: var(--background-color); }
    .header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 20px 30px;
        margin: -30px -30px 20px -30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header h1 { color: #fff; font-size: 28px; margin: 0; display: flex; align-items: center; gap: 12px; }
    .header p { color: rgba(255,255,255,0.85); font-size: 14px; margin: 5px 0 0 0; }
    [data-testid="stSidebar"] { background-color: var(--card-bg); border-right: 1px solid var(--border-color); }
    .card { background-color: var(--card-bg); border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid var(--border-color); margin-bottom: 15px; }
    .chat-message { padding: 15px 20px; border-radius: 12px; margin-bottom: 12px; line-height: 1.6; }
    .user-message { background-color: var(--primary-color); color: white; margin-left: 40px; }
    .ai-message { background-color: var(--card-bg); border: 1px solid var(--border-color); margin-right: 40px; }
    .stButton > button { background: linear-gradient(135deg, var(--accent-color) 0%, #2C9A8A 100%); color: white; border: none; border-radius: 8px; padding: 12px 24px; font-weight: 500; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(60, 174, 163, 0.4); }
    .footer { background-color: var(--primary-color); color: rgba(255,255,255,0.7); padding: 15px 30px; text-align: center; font-size: 13px; margin: 20px -30px -30px -30px; }
    .stSlider [data-baseweb="slider"] { color: var(--accent-color); }
    .stTextInput > div > div > input { background-color: var(--card-bg); border: 2px solid var(--border-color); border-radius: 8px; padding: 12px 15px; }
    .stTextInput > div > div > input:focus { border-color: var(--accent-color); box-shadow: 0 0 0 3px rgba(60, 174, 163, 0.2); }
    .stats-card { background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%); color: white; padding: 15px 20px; border-radius: 10px; text-align: center; }
    .stats-card h3 { font-size: 28px; margin: 0; }
    .stats-card p { margin: 5px 0 0 0; font-size: 12px; opacity: 0.8; }
    .section-header { color: var(--primary-color); font-size: 16px; font-weight: 600; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 2px solid var(--accent-color); }
    </style>
""", unsafe_allow_html=True)

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "MAX_TURNS" not in st.session_state:
    st.session_state.MAX_TURNS = 5
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# Initialize LLM
@st.cache_resource
def get_llm(model_name, temperature):
    return ChatOllama(model=model_name, temperature=temperature)

def build_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI Assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()

def get_response(question, temperature, model_name):
    llm = get_llm(model_name, temperature)
    chain = build_chain(llm)
    chat_history = st.session_state.chat_history
    current_turns = len(chat_history) // 2

    if current_turns >= st.session_state.MAX_TURNS:
        return "⚠️ **Context Window Full**\n\nThe AI may not follow your previous threads.\nPlease click **Clear Chat** to start fresh."

    response = chain.invoke({"question": question, "chat_history": chat_history})

    st.session_state.chat_history.append(HumanMessage(content=question))
    st.session_state.chat_history.append(AIMessage(content=response))
    st.session_state.msg_count = len(st.session_state.chat_history)

    remaining = st.session_state.MAX_TURNS - (current_turns + 1)
    return response + f"\n\n📊 **{remaining} turn(s) remaining**"

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.msg_count = 0

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Model Settings</div>', unsafe_allow_html=True)
    model_name = st.selectbox("Select Model", ["qwen3.5:cloud", "llama3.1:8b", "mistral:7b", "codellama:7b"], index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, help="Controls randomness")
    st.session_state.MAX_TURNS = st.slider("Max Conversation Turns", 3, 20, 5, 1)
    st.markdown("---")
    st.markdown('<div class="section-header">🗑️ Chat Management</div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()
    st.markdown("---")
    current_turns = len(st.session_state.chat_history) // 2
    st.markdown(f"""<div class="stats-card"><h3>{current_turns}</h3><p>Turns Used</p></div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ℹ️ About\n- **Version:** 1.0.0\n- **Framework:** LangChain + Streamlit")

# ===== HEADER =====
st.markdown("""<div class="header"><h1>🤖 AI Assistant</h1><p>Powered by LangChain & Ollama | Secure • Fast • Intelligent</p></div>""", unsafe_allow_html=True)

# ===== MAIN CONTENT =====
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 💬 Conversation")

    # Display Chat
    if len(st.session_state.chat_history) == 0:
        st.info("👋 Welcome! Start a conversation by typing below.")
    else:
        for msg in st.session_state.chat_history:
            if isinstance(msg, HumanMessage):
                st.markdown(f"""<div class="chat-message user-message"><strong>👤 You:</strong><br>{msg.content}</div>""", unsafe_allow_html=True)
            elif isinstance(msg, AIMessage):
                st.markdown(f"""<div class="chat-message ai-message"><strong>🤖 AI:</strong><br>{msg.content}</div>""", unsafe_allow_html=True)

    # Chat Input with Form (Enter key support)
    st.markdown("### ✉️ Send Message")

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("", placeholder="Type your message and press Enter...", key="user_input", label_visibility="collapsed")
        submitted = st.form_submit_button("🚀 Send", use_container_width=False)

    # Process message - check msg_count to prevent duplicates
    if submitted and user_input.strip():
        if len(st.session_state.chat_history) == st.session_state.msg_count:
            # Message not yet processed
            with st.spinner("🤔 Thinking..."):
                get_response(user_input, temperature, model_name)
            st.rerun()

with col2:
    st.markdown("### 📊 Session Info")
    current_turns = len(st.session_state.chat_history) // 2
    st.markdown(f"""<div class="card"><h4 style="margin:0;color:var(--primary-color);">Chat Statistics</h4><hr><p><strong>Messages:</strong> {len(st.session_state.chat_history)}</p><p><strong>Turns:</strong> {current_turns}/{st.session_state.MAX_TURNS}</p><p><strong>Model:</strong> {model_name}</p><p><strong>Temperature:</strong> {temperature}</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card"><h4 style="margin:0;color:var(--accent-color);">💡 Tips</h4><hr><ul style="font-size:13px;padding-left:20px;"><li>Press Enter to send</li><li>Adjust temperature for creativity</li><li>Clear chat to reset context</li><li>Use sidebar for settings</li></ul></div>""", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""<div class="footer"><p>🤖 AI Assistant | Built with LangChain & Streamlit | © 2026</p></div>""", unsafe_allow_html=True)
