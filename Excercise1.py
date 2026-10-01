from typing import Dict,TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str

def greeter(state:AgentState)->AgentState:
    """ This function compliments the user on his LangGraph journey"""
    state['message']= state['message']+", you are doing an amazing job learning LangGraph!"
    return state

graph=StateGraph(AgentState)
graph.add_node("greeter",greeter)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")
app=graph.compile()


result=app.invoke({"message":"Bob"})
print(result)