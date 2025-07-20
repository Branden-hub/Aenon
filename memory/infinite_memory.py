import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any

class InfiniteMemory:
    def __init__(self, config):
        self.config = config
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=config.get("persist_dir", "./chroma_db")
        ))
        self.collection = self.client.get_or_create_collection(name="aenon_memory")

    def store(self, context: str, content: Dict, metadata: Dict):
        # Generate an ID for the memory
        # We can use a hash of the content to avoid duplicates?
        doc_id = self._generate_id(content)
        # Embedding will be handled by ChromaDB; we just store the content as document
        self.collection.add(
            documents=[str(content)],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def retrieve(self, query: str, n_results: int = 5) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def _generate_id(self, content: Dict) -> str:
        # Simple hash for now
        return str(hash(str(content)))
