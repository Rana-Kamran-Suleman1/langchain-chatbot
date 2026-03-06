# LangChain Chatbot

An AI-powered conversational assistant built with LangChain, Ollama, and Gradio.

## Features

- **Context-aware conversations** - Maintains chat history for contextual responses
- **Configurable parameters** - Adjust temperature and max conversation turns
- **Professional UI** - Clean interface with sidebar settings
- **Built on LangChain** - Leverages LangChain's powerful abstractions

## Tech Stack

- **LangChain** - AI framework for building LLM applications
- **Ollama** - Local LLM runtime (qwen3.5:cloud model)
- **Gradio** - UI framework for ML apps

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
MODEL_NAME=qwen3.5:cloud
TEMPRATURE=0.7
MAX_TURNS=5
```

## Usage

```bash
python app.py
```

Then open `http://localhost:7860` in your browser.

## License

MIT
