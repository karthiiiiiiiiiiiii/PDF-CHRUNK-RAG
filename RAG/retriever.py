import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_faiss_index(embeddings):

    # Convert embeddings to float32
    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    # Get embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to index
    index.add(embeddings)

    return index


def search_chunks(index, query_embedding, chunks, k=3):

    # Convert query embedding
    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    # Search similar chunks
    distances, indices = index.search(
        query_embedding,
        k
    )

    retrieved_chunks = []

    for idx in indices[0]:

        # Safety check
        if 0 <= idx < len(chunks):

            retrieved_chunks.append(
                {
                    "page": chunks[idx]["page"],
                    "text": chunks[idx]["text"]
                }
            )

    return retrieved_chunks


def retrieve_relevant_chunks(query, index, chunks, k=3):

    # Convert query to embedding
    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    # Retrieve relevant chunks
    retrieved_chunks = search_chunks(
        index=index,
        query_embedding=query_embedding,
        chunks=chunks,
        k=k
    )

    return retrieved_chunks