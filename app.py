from langchain_ollama import ChatOllama

llm=ChatOllama(
    model="qwen3.5:cloud",
    temperature=0.7,
)
#           Simpe LLM Calling
response=llm.invoke("What is RAG?")
print(response.content)