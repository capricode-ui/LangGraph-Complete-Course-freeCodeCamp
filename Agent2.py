from typing import TypedDict,Dict,List,Union
from langgraph.graph import StateGraph,START,END
from langchain_core.messages  import HumanMessage,AIMessage
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
import logging
logging.getLogger("google_genai").setLevel(logging.ERROR)

class AgentState(TypedDict):
    messages:List[Union[HumanMessage,AIMessage]]

def process(state:AgentState)->AgentState:
    response=llm.invoke(state['messages'])
    state['messages'].append(AIMessage(content=response.content[0]['text']))
    print(f"\nAI:{response.content[0]['text']}")
    print(f"CURRENT_STATE:{state['messages']}")
    return state


graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

app=graph.compile()

conversation_history=[]
user_input=input("Enter message:")

while user_input!="exit":
  conversation_history.append(HumanMessage(content=user_input))
  result=app.invoke({"messages":conversation_history})
  conversation_history=result['messages']
  user_input=input("Enter message:")

with open("logging.txt","w") as file:
   file.write("Your Conversation Log:\n")

   for message in conversation_history:
      if isinstance(message,HumanMessage):
         file.write("Your Conversation Log:\n")
      elif isinstance(message,AIMessage):
         file.write(f"AI:{message.content}\n\n")
    
   file.write("End of Conversation")

print("Conversation saved to logging.txt")

