from typing import TypedDict,Dict
from langgraph.graph import StateGraph,START,END

class AgentState(TypedDict):
    number1:int
    number2:int
    final1:int
    number3:int
    number4:int
    final2:int
    operator1:str
    operator2:str


def adder_1(state:AgentState)->AgentState:
    state['final1']=state['number1']+state['number2']
    return state

def adder_2(state:AgentState)->AgentState:
    state['final2']=state['number3']+state['number4']
    return state

def subtractor_1(state:AgentState)->AgentState:
    state['final1']=state['number1']-state['number2']
    return state

def subtractor_2(state:AgentState)->AgentState:
    state['final2']=state['number3']-state['number4']
    return state

def decide1(state:AgentState)->AgentState:
    if state['operator1']=='+':
        return "addition_edge1"
    elif state['operator1']=='-':
        return "subtraction_edge1"

def decide2(state:AgentState)->AgentState:
    if state['operator2']=='+':
        return "addition_edge2"
    elif state['operator2']=='-':
        return "subtraction_edge2"


graph=StateGraph(AgentState)
graph.add_node("adder_1",adder_1)
graph.add_node("adder_2",adder_2)
graph.add_node("subtractor_1",subtractor_1)
graph.add_node("subtractor_2",subtractor_2)

graph.add_node("router1",lambda state:state)
graph.add_node("router2",lambda state:state)
#Bug fix-decide function is used with conditional edge and while adding router node the function is not decide1 and decide2 and is a lambda state:state instead
graph.add_edge(START,"router1")

graph.add_conditional_edges(
    "router1",
     decide1,
     {
         "addition_edge1":"adder_1",
         "subtraction_edge1":"subtractor_1"
     }
)
#the source is the actual node, the decider function is then used,along with the source and just the edges returned by the decider function names are used along with the destionatin node
graph.add_edge("adder_1","router2")
graph.add_edge("subtractor_1","router2")
#second phase

graph.add_conditional_edges(
    "router2",
     decide2,
     {
         "addition_edge2":"adder_2",
         "subtraction_edge2":"subtractor_2"
     }
)
graph.add_edge("adder_2",END)
graph.add_edge("subtractor_2",END)
app=graph.compile()

curr=AgentState(number1=10,number2=5,operator1="-",number3=7,number4=2,operator2='+',final1=0,final2=0)
result=app.invoke(curr)
print(result)