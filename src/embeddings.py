from sentence_transformers import SentenceTransformer

model = None


def create_embeddings(chunks):

    global model

    if model is None:

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        return model.encode(chunks)

     