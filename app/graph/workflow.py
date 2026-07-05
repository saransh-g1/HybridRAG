from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    context_node,
    crag_node,
    generation_node,
    hyde_node,
    retrieval_node,
    self_rag_node,
    retry_retrieval_node,
    retry_generation_node,
)
from app.graph.state import GraphState


def route_after_crag(state: GraphState):

    if state["retrieval_good"]:
        return "generate"

    return END


def route_after_selfrag(state: GraphState):

    if state["supported"]:
        return END

    return END


class GraphWorkflow:

    def __init__(self):

        builder = StateGraph(GraphState)

        builder.add_node("hyde", hyde_node)
        builder.add_node("retrieve", retrieval_node)
        builder.add_node("context", context_node)
        builder.add_node("crag", crag_node)
        builder.add_node("generate", generation_node)
        builder.add_node("selfrag", self_rag_node)
        builder.add_node("retry_retrieval", retry_retrieval_node)
        builder.add_node("retry_generation", retry_generation_node)

        builder.add_edge("hyde", "retrieve")
        builder.add_edge("retrieve", "context")
        builder.add_edge("context", "crag")
        builder.add_edge("retry_retrieval", "retrieve")
        builder.add_edge("retry_generation", "generate")
        builder.add_node(
            "router",
            router_node,
        )

        builder.add_node(
            "sql",
            sql_node,
        )

        builder.add_edge(
            START,
            "router",
        )

        builder.add_conditional_edges(
            "router",
            route_question,
            {
                "hyde": "hyde",
                "sql": "sql",
            },
        )

        builder.add_edge(
            "sql",
            END,
        )
        builder.add_conditional_edges(
            "retrieve",
            route_after_crag,
            {
                "context": "context",
                "retry_retrieval": "retry_retrieval",
                END: END,
            },
        )

        builder.add_conditional_edges(
            "selfrag",
            route_after_selfrag,
            {
                "retry_generation": "retry_generation",
                END: END,
            },
        )

        self.graph = builder.compile()

    def invoke(self, question: str):

        state = GraphState(
            question=question,
            retrieval_query=question,
            chunks=[],
            scores=[],
            context="",
            answer="",
            retrieval_good=False,
            supported=False,
            retrieval_attempts=0,
            generation_attempts=0,
        )

        result = self.graph.invoke(state)

        return result


@lru_cache
def get_graph():

    return GraphWorkflow()