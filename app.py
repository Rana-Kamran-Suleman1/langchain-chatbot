import gradio as gr
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
import os
from dotenv import load_dotenv

# Initialize LLM
llm = ChatOllama(
    model=os.getenv("MODEL_NAME"),
    temperature=os.getenv("TEMPRATURE"),
)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI Assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# Create chain
chain = prompt | llm | StrOutputParser()

# Chat history storage
chat_history = []
MAX_TURNS = os.getenv("MAX_TURNS")


def chat(question, history):
    """Process chat message and return response."""
    global chat_history
    current_turns = len(chat_history) // 2

    if current_turns >= MAX_TURNS:
        new_message = {"role": "user", "content": question}
        ai_message = {"role": "assistant", "content": "Your Context Window is full. The AI may not follow your previous threads. Please click 'Clear Chat' for a new chat."}
        return history + [new_message, ai_message]

    try:
        response = chain.invoke({
            "question": question,
            "chat_history": chat_history
        })
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=response))
        remaining = MAX_TURNS - (current_turns + 1)
        response += f"\n\n⚠️ Warning: Only {remaining} turn(s) left"

        new_message = {"role": "user", "content": question}
        ai_message = {"role": "assistant", "content": response}
        return history + [new_message, ai_message]
    except Exception as e:
        new_message = {"role": "user", "content": question}
        ai_message = {"role": "assistant", "content": f"Error: {str(e)}"}
        return history + [new_message, ai_message]


def clear_chat():
    """Clear chat history and reset."""
    global chat_history
    chat_history.clear()
    return []


def update_temperature(temp):
    """Update LLM temperature."""
    global llm
    llm = ChatOllama(
        model="qwen3.5:cloud",
        temperature=temp,
    )


def update_max_turns(turns):
    """Update max turns."""
    global MAX_TURNS
    MAX_TURNS = int(turns)


# Build Gradio UI
with gr.Blocks(
    title="LangChain Chatbot",
    theme=gr.themes.Soft()
) as demo:

    # Custom CSS
    gr.Markdown("""
    <style>
    .header-section {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer-section {
        text-align: center;
        padding: 15px;
        background: #f0f0f0;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 12px;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """)

    # Header
    gr.HTML("""
    <div class="header-section">
        <h1>🤖 LangChain Chatbot</h1>
        <p>AI-powered conversational assistant with context memory</p>
    </div>
    """)

    with gr.Row():
        # Sidebar with settings
        with gr.Column(scale=1, elem_classes=["sidebar-section"]):
            gr.Markdown("### ⚙️ Settings")
            gr.Markdown("Configure your chatbot preferences")

            temperature_slider = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=0.7,
                step=0.1,
                label="🌡️ Temperature",
                info="Controls randomness (0=focused, 2=creative)"
            )
            temperature_slider.change(update_temperature, inputs=[temperature_slider])

            max_turns_slider = gr.Slider(
                minimum=1,
                maximum=20,
                value=5,
                step=1,
                label="🔄 Max Turns",
                info="Maximum conversation turns before reset"
            )
            max_turns_slider.change(update_max_turns, inputs=[max_turns_slider])

            gr.Markdown("---")
            gr.Markdown("### ℹ️ Info")
            gr.Markdown(f"**Model:** qwen3.5:cloud")
            gr.Markdown(f"**Max Turns:** {MAX_TURNS}")

        # Main chat section
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Chat History",
                height=500
            )

            with gr.Row():
                msg_input = gr.Textbox(
                    show_label=False,
                    placeholder="Type your message here...",
                    container=False,
                    scale=4,
                )
                submit_btn = gr.Button("Send", variant="primary", scale=1)

            with gr.Row():
                clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")

    # Footer
    gr.HTML("""
    <div class="footer-section">
        <p>LangChain Chatbot | Powered by Ollama & Gradio</p>
        <p>Built with LangChain Framework</p>
    </div>
    """)

    # Event handlers
    def submit_message(msg, history):
        if msg.strip():
            return "", chat(msg, history)
        return msg, history

    # Bind events
    submit_btn.click(submit_message, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
    msg_input.submit(submit_message, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
    clear_btn.click(clear_chat, outputs=[chatbot])

# Launch the app
if __name__ == "__main__":
    demo.launch()
