import re
import json
from typing import TypedDict


from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import PGVector
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI


from src.config import api_key, vector_db_connection_string, vector_db_collection_name
from src.prompts import EnhanceRetrievalPrompt, KnowledgeAnswerPrompt
from src.embedding import SiliconFlowEmbedding
from src.reranker import SiliconFlowReranker


llm1 = ChatOpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1/", 
    model="deepseek-ai/DeepSeek-V3",
)


llm2 = ChatOpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1/", 
    model="deepseek-ai/DeepSeek-V3",
    streaming = True,
    callbacks = [StreamingStdOutCallbackHandler()]
)


embedding_model = SiliconFlowEmbedding(
    api_key = api_key,
    model_name = "BAAI/bge-m3"
)

rarank_model = SiliconFlowReranker(
    api_key = api_key,
    model_name = "BAAI/bge-reranker-v2-m3"
)

vector_db = PGVector(
    embedding_function=embedding_model,
    collection_name=vector_db_collection_name,
    connection_string=vector_db_connection_string,
)


def llm_enhance_retrieval(state) -> dict:
    
    query = state["query"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", EnhanceRetrievalPrompt.system),
        ("user", "{query}")
    ])

    response = llm1.invoke(prompt.format(query=query))
    return {"llm_text": response.content}


def llm_answer(state):
    query = state["query"]
    retrieve_result = state["retrieve_result"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", KnowledgeAnswerPrompt.system),
        ("user", "{query}")
    ])

    text = ""
    for chunk in llm2.stream(
        prompt.format(query=query, 
                      knowledge="\n".join(retrieve_result))
        ):
        text += chunk.text()
        yield {"stream_answer": chunk.text()}

    yield {"full_answer": text}




def script_llmtext2obj(state):
    searches = [state["query"], ]
    text = state["llm_text"]

    try:
        try:
            res = json.loads(text)
        except:
            pattern = r'\{[^{}]*\}'
            match = re.search(pattern, text)
            match_str = match.group() if match else None
            res = json.loads(match_str)

        searches += res.get("search", [])

        return {
            "search":searches
        }

    except:
        return  {
            "search":searches
        }
    
def knowledge_retrieve(state):
    searches = state["search"]
    query = state["query"]

    data = []
    for s in searches:
        data += vector_db.similarity_search(s, k=10)
    data = [d.page_content for d in data]


    data = rarank_model.rerank(
        query=query,
        documents=data,
        top_k=5
    )

    return {"retrieve_result":data}

class GraphState(TypedDict):
    query: str
    llm_text:str
    search: str
    retrieve_result: list
    answer: str
    full_answer:str



class MiniRag():
    def __init__(self,):

        workflow = StateGraph(state_schema=GraphState)
        workflow.add_node("node1", llm_enhance_retrieval)
        workflow.add_node("node2", script_llmtext2obj)
        workflow.add_node("node3", knowledge_retrieve)
        workflow.add_node("node4", llm_answer)
        workflow.add_edge("node1", "node2")
        workflow.add_edge("node2", "node3")
        workflow.add_edge("node3", "node4")

        workflow.set_entry_point("node1")
        workflow.set_finish_point("node2")
        app = workflow.compile()

        self.app = app


    def invoke(self, query):
        for chunk in self.app.stream({"query":query}, stream_mode="updates"):
            yield chunk

        
