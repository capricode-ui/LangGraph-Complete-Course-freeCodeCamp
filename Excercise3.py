from typing import Dict,TypedDict,List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name:str
    age:int
    skills:List[str]
    final:str

def first_node(state:AgentState)->AgentState:
    state['final']=f"Hey,{state['name']}!You are {state['age']} years old."
    return state

def second_node(state:AgentState)->AgentState:
    state['final']+=f"Your skills are:{', '.join(state['skills'])}."
    return state

graph=StateGraph(AgentState)
graph.add_node("first_node",first_node)
graph.add_node("second_node",second_node)
graph.set_entry_point("first_node")
graph.set_finish_point("second_node")
graph.add_edge("first_node","second_node")
app=graph.compile()

result=app.invoke({'name':'Jack','age':18,'skills':['Java','C++','Python']})
print(result['final'])