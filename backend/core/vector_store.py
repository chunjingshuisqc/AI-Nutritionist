import uuid
from typing import Dict, List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from .config import settings
from .llm_client import llm_client


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    async def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]

        embeddings = await llm_client.embed(documents)

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas or [{} for _ in documents],
            ids=ids
        )

        return ids

    async def search(
        self,
        query: str,
        top_k: int = None,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        top_k = top_k or settings.TOP_K

        query_embedding = (await llm_client.embed([query]))[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict,
            include=["documents", "metadatas", "distances"]
        )

        docs = []

        if results and results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                docs.append({
                    "content": doc,
                    "metadata": (
                        results["metadatas"][0][i]
                        if results["metadatas"]
                        else {}
                    ),
                    "score": (
                        1 - results["distances"][0][i]
                        if results["distances"]
                        else 0
                    )
                })

        return docs

    def get_count(self) -> int:
        return self.collection.count()


vector_store = VectorStore()