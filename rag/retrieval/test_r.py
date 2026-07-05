from rag.retrieval.retriever import Retriever

r = Retriever()

docs = r.retrieve(
    "What is Kubernetes?"
)

print(docs)