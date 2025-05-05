## NeuroAdventure - API

The repository contains a conceptual materials for a chatbot designed specifically for neurodivergent children. The chat emphasize emotional and social context of messages sent by a child using AI.

Conceptual materials:
1. LLM chatbot for children - [Go to Jupyter file](concepts/1.%20children_chat.ipynb)

The abovementioned conceptual materials are moved to [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)

To run a LangGraph Studio and use the AI agent mentioned in conceptual materials, do the following:

First, provide environment variables in the root directory, as well as in the directory called './api/langgraph-app'

1. Create a python virtual environment in root directory via:
```bash
python3 -m venv neuroadventure-env
```
2. Start the virtual environment via:
```bash
source neuroadventure-env/bin/activate
```
3. Install required packages with:
```bash
pip install -r requirements.txt
```
4. Change directory to:
```bash
cd /api/langgraph-app
```
5. Install the agents as packages with:
```bash
pip install -e .
```
6. Start Langgraph Studio via:
```bash
langgraph dev
```