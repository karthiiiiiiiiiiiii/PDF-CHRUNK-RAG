from sentence_transformers import SentenceTransformer
import numpy as np

# Load local embedding model
model = SentenceTransformer("models/all-MiniLM-L6-v2")


def create_embeddings(chunks):

    # Extract text from chunks
    texts = [chunk["text"] for chunk in chunks]

    # Generate embeddings
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    # Convert to float32 for FAISS
    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    return embeddings