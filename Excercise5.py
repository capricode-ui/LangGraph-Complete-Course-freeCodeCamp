from typing import Dict,TypedDict,List
from langgraph.graph import StateGraph,START,END
import random


# {"player_name": "Student", "guesses": [], "attempts": 0, "lower_bound": 1, 
#"upper_bound": 20,target
class AgentState(TypedDict):
    player_name:str
    guesses:List[int]
    attempts:int
    lower_bound:int
    upper_bound:int
    target:int
    guess:int


def setup_node(state:AgentState)->AgentState:
    state['player_name']="Student"
    state['guesses']=[]
    state['attempts']=0
    state['lower_bound']=1
    state['upper_bound']=20
    state['target']=5
    return state


def guess_node(state:AgentState)->AgentState:
    state['guesses'].append(random.randint(state['lower_bound'],state['upper_bound']))
    return state

def check(state:AgentState)->AgentState:
    if len(state['guesses'])>7:
        print("Max guess limit reached")
        print(f"Guesses were {state['guesses']}.")
        return 'END'
    if state['guesses'][-1]==state['target']:
        print(f"Number was found.It was {state['guesses'][-1]}")
        print(f"Guesses were {state['guesses']}.")
        return 'END'
    else:
        return 'continue'
    
def hint_node(state:AgentState)->AgentState:
    if state['guesses'][-1]>state['target']:
        print('Target is lower')
        state['upper_bound']=state['guesses'][-1]-1
    elif state['guesses'][-1]<state['target']:
        print('Target is higher')
        state['lower_bound']=state['guesses'][-1]+1
    return state


graph=StateGraph(AgentState)
graph.add_node('setup_node',setup_node)
graph.add_node('guess_node',guess_node)
graph.add_node('hint_node',hint_node)
graph.add_edge(START,'setup_node')
graph.add_edge('setup_node','guess_node')
graph.add_edge('guess_node','hint_node')
graph.add_conditional_edges(
    'hint_node',
    check,
    {
        'continue':'guess_node',
        'END':END
    }
)
app=graph.compile()


result=app.invoke( {"player_name": "Student", "guesses": [], "attempts": 0, "lower_bound": 1, 
"upper_bound": 20})


    