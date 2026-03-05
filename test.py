from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder    #For Temoprary Storage

llm=ChatOllama(
    model="qwen3.5:cloud",
    temperature=0.7,
)

prompt=ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI Assistent.",),
     MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()
chat_history=[]
MAX_TURNS=5

def chat(question):
    current_turns=len(chat_history) // 2
    if current_turns >= MAX_TURNS:
        return(
            "Your Context Window is full", 
            "the AI may not follow your prev threads.",
            "please type clear for new chat"
        )
        
    response=chain.invoke({
        "question" : question,
        "chat_history" : chat_history 
        })
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))
    remaining = MAX_TURNS - (current_turns + 1)
    
    response += f"\n\nWarning: Only {remaining} turn(s) left]"
    return response

def main():
    print("Langchain Chatbot Ready! (type 'exit' to quit) type 'clear' to reset context")
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Exiting chatbot. Goodbye!")
            break
        if user_input.lower() == "clear":
            chat_history.clear()
            print("Chat history cleared. Starting fresh!")
            continue
        print(f"AI: {chat(user_input)}")

main()
