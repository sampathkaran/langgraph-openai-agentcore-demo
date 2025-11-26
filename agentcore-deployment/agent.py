from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from typing import TypedDict, Annotated, List
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from bedrock_agentcore.runtime import BedrockAgentCoreApp # import bedrock runtime
import boto3
import os
import json

client = boto3.client("secretsmanager")
response = client.get_secret_value(SecretId="openai-api-key") # input the secret name
secret_json =json.loads(response["SecretString"])
api_key = secret_json["api-key"] # input the key name of the secret

#Intialize the bedrock
aws_app = BedrockAgentCoreApp()


# Define tool
websearch_tool = DuckDuckGoSearchResults()
tools = [websearch_tool]

llm_tools = ChatOpenAI(model="gpt-5-nano",api_key=api_key).bind_tools(tools=tools)

#define the state schema
class AgentState(TypedDict):
    messages : Annotated[list, add_messages] # this class will basically append the messages instead of overwriting

#create the agent node
def llm_node(state: AgentState)-> AgentState:
    # print (state ['messages'])
    response = llm_tools.invoke(state ['messages'])
    # print(response)
    return {"messages" : response}

# create the graph

graph = StateGraph(AgentState)
graph.add_node("llm_node", llm_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "llm_node")
graph.add_conditional_edges("llm_node", tools_condition)
graph.add_edge("tools", "llm_node")
graph.add_edge("llm_node", END)

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="tools-pic.png")


@aws_app.entrypoint
def langgraph_bedrock(payload):
    """ Invoke the agent with the payload"""
    user_input = payload.get('messages') # read the data from payload dictonary using the key prompt
    # Wrap it properly for LangGraph
    state_input = {"messages": [HumanMessage(content=user_input)]}
    result = app.invoke(state_input)
    return result['messages'][-1].content

if __name__== "__main__":
    print(langgraph_bedrock({"messages": "Who won the formula1 singapore 2025? give the answer briefly "}))
    #aws_app.run() # This starts the http server on port 8080
  