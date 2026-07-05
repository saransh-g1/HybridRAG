from app.graph.state import GraphState

from app.services.hyde_service import get_hyde_service
from app.services.hybrid_retrieval_service import HybridRetrievalService
from app.services.crag_service import get_crag_service
from app.services.self_rag_service import get_self_rag
from app.services.llm_service import LLMService
from app.services.router_service import get_router
from app.services.sql.sql_agent import get_sql_agent

sql_agent = get_sql_agent()

router = get_router()

hyde = get_hyde_service()

retriever = HybridRetrievalService()

crag = get_crag_service()

self_rag = get_self_rag()

llm = LLMService()

MAX_RETRIEVAL_RETRIES = 2
MAX_GENERATION_RETRIES = 2

def hyde_node(state: GraphState):

    retrieval_query = hyde.generate(
        state["question"]
    )

    state["retrieval_query"] = retrieval_query

    return state

def retrieval_node(state: GraphState):

    result = retriever.retrieve(
        state["retrieval_query"]
    )

    state["retrieval_good"] = (
        result["status"] == "SUCCESS"
    )

    state["chunks"] = [
    item.chunk
    for item in result["chunks"]
    ]

    state["scores"] = [
        float(item.score)
        for item in result["chunks"]
    ]

    return state

def context_node(state: GraphState):

    state["context"] = "\n\n".join(
        chunk.text
        for chunk in state["chunks"]
    )

    return state


def generation_node(state: GraphState):

    prompt = f"""
Answer the user's question using ONLY the context.

Context:

{state["context"]}

Question:

{state["question"]}
"""

    answer = llm.generate(prompt)

    state["answer"] = answer

    return state


def crag_node(state: GraphState):

    good = crag.is_context_good(
        state["scores"]
    )

    state["retrieval_good"] = good

    return state


def self_rag_node(state: GraphState):

    result = self_rag.evaluate(

        state["question"],

        state["context"],

        state["answer"]

    )

    state["supported"] = result["supported"]

    return state

def route_after_crag(state):

    if state["retrieval_good"]:
        return "context"

    if state["retrieval_attempts"] >= MAX_RETRIEVAL_RETRIES:
        return END

    return "retry_retrieval"

def route_after_crag(state):

    if state["retrieval_good"]:
        return "context"

    if state["retrieval_attempts"] >= MAX_RETRIEVAL_RETRIES:
        return END

    return "retry_retrieval"

def retry_retrieval_node(state: GraphState):

    state["retrieval_attempts"] += 1

    return state

def retry_generation_node(state: GraphState):

    state["generation_attempts"] += 1

    return state

def router_node(state: GraphState):

    state["route"] = router.route(
        state["question"]
    )

    return state


def sql_node(state: GraphState):

    state["answer"] = sql_agent.answer(
        state["question"]
    )

    return state

def route_question(state):

    if state["route"] == "SQL":
        return "sql"

    return "hyde"