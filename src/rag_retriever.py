import faiss
import json
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def retrieve_relevant_chunks(query):

    index = faiss.read_index(
        "data/vector_index.faiss"
    )

    with open(
        "data/chunks.json",
        "r",
        encoding="utf-8"
    ) as file:

        chunks = json.load(file)

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
    query_embedding,
    3
    )

    results = []

    for i in indices[0]:

        results.append(
        chunks[i]
        )

    return results