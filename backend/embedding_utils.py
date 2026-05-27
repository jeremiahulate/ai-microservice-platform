from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

model = SentenceTransformer("all-MiniLM-L6-v2")

qdrant = QdrantClient(host="qdrant", port=6333)

COLLECTION_NAME = "documents"

def create_collection():
    existing = qdrant.get_collections().collections
    names = [c.name for c in existing]

    if COLLECTION_NAME not in names:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            ),
        )

def chunk_text(text, chunk_size=200):
    words = text.split()

    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

def embed_document(document_id, filename, text):
    create_collection()

    chunks = chunk_text(text)

    embeddings = model.encode(chunks)

    points = []

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": idx,
                    "text": chunk,
                }
            )
        )
    
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)

def search_documents(query, limit=5):
    query_embedding = model.encode(query).tolist()

    response = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
    )
    
    results = response.points

    return [
        {
            "score": point.score,
            "text": point.payload["text"],
            "filename": point.payload["filename"]
        }
        for point in results
    ]