from typing import TypedDict,Dict,List
from langgraph.graph import StateGraph,START,END
from langchain_core.messages  import HumanMessage
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
import logging
logging.getLogger("google_genai").setLevel(logging.ERROR)

class AgentState(TypedDict):
    messages:List[HumanMessage]

def process(state:AgentState)->AgentState:
    response=llm.invoke(state['messages'])
    print(f"\nAI:{response.content[0]['text']}")
    return state


graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

app=graph.compile()

user_input=input("Enter message:")

while user_input!="exit":
  app.invoke({"messages":[HumanMessage(content=user_input)]})
  user_input=input("Enter message:")
print("GoodBye")
  