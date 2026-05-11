from langgraph.graph import StateGraph,START, END
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import BaseMessage, HumanMessage
import operator


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=1.0)

class Chatstate(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def chatting(state: Chatstate):
    result = model.invoke(state['messages'])
    return {"messages": [result]}

checkpointer = InMemorySaver()
graph = StateGraph(Chatstate)
graph.add_node("chatting", chatting)

graph.add_edge(START,"chatting")
graph.add_edge("chatting", END)

chatbot = graph.compile(checkpointer=checkpointer)
