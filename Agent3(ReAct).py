from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,ToolMessage,SystemMessage
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]


@tool
def add(a:int,b:int):
    """ This tool adds numbers a and b together"""
    return a+b

@tool
def subtract(a:int,b:int):
    """This tool subtracts two numbers a and b."""
    return a-b

@tool
def multiply(a:int,b:int):
    """ This tool multiplies two numbers"""
    return a*b


tools=[add,subtract,multiply]
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite").bind_tools(tools)

def modelCall(state:AgentState)->AgentState:
    system_prompt=SystemMessage(content='You are a helpful AI assistant with the ability to use tools')
    response=llm.invoke([system_prompt]+state['messages'])
    return {'messages':[response]}


def should_continue(state:AgentState)->AgentState:
    if not state['messages'][-1].tool_calls:
        return 'end'
    else:
        return 'continue'

graph=StateGraph(AgentState)
graph.add_node("modelCall",modelCall)
tool_node=ToolNode(tools=tools)
graph.add_node("tool_node",tool_node)
graph.add_edge(START,"modelCall")
graph.add_conditional_edges(
    "modelCall",
    should_continue,
    {
        "continue":"tool_node",
        "end":END
    }
)
graph.add_edge("tool_node","modelCall")
app=graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))