"""
ChoreoAI Example: Embeddings and Simple RAG

This example demonstrates how to use ChoreoAI for creating embeddings
and implementing a simple Retrieval-Augmented Generation (RAG) system.

Requirements:
- Run: ./setup.sh (to create virtual environment and install dependencies)
- Set OPENAI_API_KEY environment variable
- ChoreoAI server running on http://localhost:8000
"""

import os
import numpy as np
from openai import OpenAI


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def main():
    """Embeddings and simple RAG example."""

    print("=" * 60)
    print("ChoreoAI Example: Embeddings & Simple RAG")
    print("=" * 60)
    print()

    # Initialize OpenAI client with ChoreoAI base URL
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="http://localhost:8000/v1"
    )

    # Knowledge base: Simple documents about ChoreoAI
    documents = [
        "ChoreoAI is a unified API orchestration platform for multiple AI providers.",
        "ChoreoAI supports OpenAI, Claude, Gemini, and other AI models.",
        "ChoreoAI provides features like load balancing, failover, and cost optimization.",
        "ChoreoAI uses FastAPI and is deployed with Docker containers.",
        "Python is a popular programming language for AI and machine learning."
    ]

    print("=Ú Knowledge Base:")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc}")
    print()

    # Step 1: Create embeddings for all documents
    print("= Creating embeddings for knowledge base...")
    try:
        embeddings_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=documents
        )

        # Extract embeddings
        doc_embeddings = [item.embedding for item in embeddings_response.data]
        print(f" Created {len(doc_embeddings)} embeddings")
        print(f"   Embedding dimension: {len(doc_embeddings[0])}")
        print()

    except Exception as e:
        print(f"L Error creating embeddings: {e}")
        return 1

    # Step 2: Query the knowledge base
    query = "What providers does ChoreoAI support?"
    print(f"S Query: '{query}'")
    print()

    print("= Creating embedding for query...")
    try:
        query_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        query_embedding = query_response.data[0].embedding
        print(" Query embedding created")
        print()

    except Exception as e:
        print(f"L Error creating query embedding: {e}")
        return 1

    # Step 3: Find most similar documents
    print("= Finding most relevant documents...")
    similarities = []
    for i, doc_emb in enumerate(doc_embeddings):
        similarity = cosine_similarity(query_embedding, doc_emb)
        similarities.append((i, similarity, documents[i]))

    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)

    print()
    print("=Ê Top 3 most relevant documents:")
    print("-" * 60)
    for i, (doc_idx, sim, doc) in enumerate(similarities[:3], 1):
        print(f"{i}. Similarity: {sim:.4f}")
        print(f"   {doc}")
        print()

    # Step 4: Use top result for RAG
    most_relevant = similarities[0][2]
    print("=" * 60)
    print("> Generating answer using RAG...")
    print()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Answer the question based on this context: {most_relevant}"
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            max_tokens=100
        )

        answer = response.choices[0].message.content
        print("=Ý Answer:")
        print("-" * 60)
        print(answer)
        print("-" * 60)
        print()
        print("( Success! RAG pipeline completed.")

    except Exception as e:
        print(f"L Error generating answer: {e}")
        return 1

    print()
    print("=" * 60)

    return 0


if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("L Error: OPENAI_API_KEY environment variable not set")
        print()
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY=sk-your-key-here")
        print()
        exit(1)

    # Check if numpy is installed
    try:
        import numpy as np
    except ImportError:
        print("L Error: NumPy is not installed")
        print()
        print("Install it with: pip install numpy")
        print()
        exit(1)

    exit(main())
