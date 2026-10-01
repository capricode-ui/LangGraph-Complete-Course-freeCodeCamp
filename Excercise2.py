from typing import Dict,TypedDict,List
from langgraph.graph import StateGraph
import math

class AgentState(TypedDict):
    
    name:str
    values:List[int]
    operator:str
    result:str


def calculate(state:AgentState)->AgentState:
    if state['operator']=="+":
        state['result']=f"Hi {state['name']}! The sum of values is {sum(state['values'])}."
    elif state['operator']=="*":
        state['result']=f"Hi {state['name']}! The sum of values is {math.prod(state['values'])}."
    return state

graph=StateGraph(AgentState)
graph.add_node("calculate",calculate)
graph.set_entry_point("calculate")
graph.set_finish_point("calculate")
app=graph.compile()

result1=app.invoke({"name":"Steve","values":[1,2,3,4,5],'operator':'+'})
result2=app.invoke({"name":"Steve","values":[1,2,3,4,5],'operator':'*'})


print(result1['result'])
print(result2['result'])