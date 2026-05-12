from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated
import operator

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=1.0)

class chatState(TypedDict):
    messages: Annotated[list[str], operator.add]

def chat(state: chatState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

checkpointer = InMemorySaver()
graph = StateGraph(chatState)
graph.add_node("chat", chat)
graph.add_edge(START,"chat")
graph.add_edge("chat",END)

chatbot = graph.compile(checkpointer=checkpointer)