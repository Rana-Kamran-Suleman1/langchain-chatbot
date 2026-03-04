from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm=ChatOllama(
    model="qwen3.5:cloud",
    temperature=0.7,
)
#           Method 1
# messages=[
#     SystemMessage(content="You are a web devloper"),
#     HumanMessage(content="How Much Backend languages you can use in website creation?")
# ]


#           Method 2
# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
#           Method 3
# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     HumanMessage(content="How Much Backend languages you can use in website creation?")
# ]
# ai_msg = llm.invoke(prompt)
# ai_msg
prompt=ChatPromptTemplate.from_messages([
     (
        "system",
        "You are a web developer",
    ),
    ("human", "{question}"),
])
chain = prompt | llm | StrOutputParser()
# response=chain.invoke({"question" : "How Much Backend languages you can use in website creation?" })
# print(response)
# response=llm.invoke(prompt)
# print(response.content)
#           Simpe LLM Calling
# response=llm.invoke("What is RAG?")
# print(response.content)

for chunk in chain.stream({"question" : "How Much Backend languages you can use in website creation?" }):
    print(chunk, end="", flush=True)