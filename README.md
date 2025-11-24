# Plug and Productionize your AI agents with AWS Bedrock AgentCore

### Description

This repository provides a simple way to deploy locally developed AI agents using AWS Bedrock AgentCore.

I have created a basic LLM agent (single node) using an OpenAI model. As LLMs are limited to the knowledge contained in their training data, I integrated a tool to extend its capabilities: the DuckDuckGoSearchResults tool from LangChain, which allows the agent to retrieve up-to-date information.

Next, we’ll see how just a few lines of code make it possible to connect our agent to AWS AgentCore and deploy it in minutes.



| Tech Stack                     | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| Open AI                        | Model: gpt-5-nano                                                           |
| Agent Framework                | Langgraph                                                                   |
| Deployment                     | AWS Bedrock AgentCore                                                       |
| AI tool                        | DuckDuckGoSearchResults                                                     |


## Project folder structure

langgraph-openai-agentcore-demo/
├── README.md
├── agentcore-deployment/
│   ├── agent.py
│   └── requirements.txt
└── secret-policy.json

## Local Installation Steps & Testing

Follow these steps to set up the project:

1. Create the virtual environment using conda

```bash
conda create -n agentcore python=3.10
```

2. Install the requirements file 

```bash
pip install -r requirements.txt
```

3. As the OpenAI model requires an API key at runtime, the recommended best practice is to store the key securely in AWS Secrets Manager. During runtime, we can use a boto3 client to fetch the secret.

Steps to store your API key in AWS Secrets Manager:

- Go to AWS Console → Secrets Manager → Store a new secret

- Select Other type of secret

- Enter the key as ```api-key``` and provide your API key value

- Click Next

- Name your secret ```my-api-key```

- Click Next, then Store
  

3. Next we will test the code locally by python command with a prompt input.
   - Change directory to agencore-deployment & edit the file ```agent.py``` 
 ```bash
        cd agentcore-deployment       
``` 
   - Uncomment the print statement line as below and comment the ```aws_app.run()``` line 
   - Input your desired query in the print statement to see the output, keep the messages key as it is and only update the value
        e.g. ```print(langgraph_bedrock({"messages": "Who won the formula1 race in singapore 2025? give the answer briefly"}))```

   Before:
   ![alt text](image.png)

   After:
   ![alt text](image-1.png)

   - Execute the code now
```bash  
       python agent.py 
```

## Architecture

When a query is passed to the LLM, it first checks whether it already has the information needed to answer. If not, it triggers a tool call to the DuckDuckGoSearchResults web search tool to retrieve the required data. The agent may loop through this process, calling the web search tool multiple times until it gathers enough information. Once satisfied, the LLM generates the final response.

![alt text](image-2.png)

## Deployment to AWS Bedrock AgentCore