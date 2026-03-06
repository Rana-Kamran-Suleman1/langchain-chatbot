# CLAUDE.md - Project Workflow

## Project Overview
LangChain Chatbot - AI-powered conversational assistant with context memory built using LangChain, Ollama, and Gradio.

## Tech Stack
- **LangChain** - AI framework for LLM applications
- **Ollama** - Local LLM runtime (qwen3.5:cloud model)
- **Gradio** - UI framework for ML apps
- **Python** - Programming language

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         APPLICATION FLOW                            │
└─────────────────────────────────────────────────────────────────────┘

1. ENVIRONMENT SETUP
   └── load_dotenv() → reads .env file
       ├── MODEL_NAME=qwen3.5:cloud
       ├── TEMPERATURE=0.7
       └── MAX_TURNS=5

2. LLM INITIALIZATION
   └── ChatOllama(model, temperature)
       └── Creates LLM instance with config

3. CHAIN CONSTRUCTION
   └── prompt | llm | StrOutputParser()
       ├── ChatPromptTemplate (system + history + human)
       ├── ChatOllama (LLM)
       └── StrOutputParser (output parsing)

4. UI BUILD (Gradio)
   └── gr.Blocks
       ├── Header (HTML with gradient)
       ├── Row
       │   ├── Sidebar (settings)
       │   │   ├── Temperature slider (0.0-2.0)
       │   │   └── Max Turns slider (1-20)
       │   └── Main chat
       │       ├── gr.Chatbot (history display)
       │       ├── Textbox (input)
       │       └── Buttons (Send, Clear Chat)
       └── Footer (HTML)

5. EVENT HANDLERS
   ├── submit_btn.click → submit_message()
   ├── msg_input.submit → submit_message()
   └── clear_btn.click → clear_chat()

6. CHAT FLOW (per message)
   ┌─────────────────────────────────────────┐
   │  User输入question                        │
   └─────────────────┬───────────────────────┘
                     ▼
   ┌─────────────────────────────────────────┐
   │  Check: current_turns >= MAX_TURNS?    │
   │  If YES → Return "Context Window full"  │
   └─────────────────┬───────────────────────┘
                     ▼ (NO)
   ┌─────────────────────────────────────────┐
   │  chain.invoke({                         │
   │    "question": question,                │
   │    "chat_history": chat_history         │
   │  })                                     │
   └─────────────────┬───────────────────────┘
                     ▼
   ┌─────────────────────────────────────────┐
   │  Append to chat_history:                │
   │  - HumanMessage(content=question)       │
   │  - AIMessage(content=response)           │
   └─────────────────┬───────────────────────┘
                     ▼
   ┌─────────────────────────────────────────┐
   │  Return updated history + warning       │
   │  (remaining turns)                      │
   └─────────────────────────────────────────┘
```

## Setup

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file**
   ```
   MODEL_NAME=qwen3.5:cloud
   TEMPERATURE=0.7
   MAX_TURNS=5
   ```

4. **Ensure Ollama is running**
   ```bash
   ollama serve
   ollama pull qwen3.5:cloud
   ```

## Run

```bash
python app.py
```

Open http://localhost:7860 in browser.

## Key Files
- `app.py` - Main application with Gradio UI and LangChain logic
- `requirements.txt` - Dependencies
- `.env` - Configuration (create this file)
- `CLAUDE.md` - This file

## Configuration Options
| Variable | Default | Description |
|----------|---------|-------------|
| MODEL_NAME | qwen3.5:cloud | Ollama model to use |
| TEMPERATURE | 0.7 | LLM creativity (0=focused, 2=creative) |
| MAX_TURNS | 5 | Max conversation turns before reset |
