import time
import chromadb
from chromadb.config import Settings

class MemorySystem:
    def __init__(self, stm_capacity=10000, stm_expiry=3600):
        self.stm = {}  # Short-term memory (cache-like) with expiry
        self.ltm_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./ltm"))
        self.ltm_collection = self.ltm_client.create_collection("aenon_ltm")
        self.stm_capacity = stm_capacity
        self.stm_expiry = stm_expiry
        
    def add_memory(self, data, modality, context=None):
        """Add a memory with modality (text, vision, audio, etc.)."""
        # Generate an embedding from the data (using a pre-trained model, placeholder)
        embedding = self._embed(data, modality)
        # Store in STM and then asynchronously to LTM
        self._add_to_stm(data, embedding, context)
        self._add_to_ltm(embedding, data, context)
    
    def retrieve(self, query, modality, top_k=5):
        """Retrieve memories relevant to the query."""
        query_embedding = self._embed(query, modality)
        results = self.ltm_collection.query(query_embeddings=[query_embedding], n_results=top_k)
        return results
    
    def _embed(self, data, modality):
        # Placeholder: use a multimodal embedding model based on modality
        return [0.1] * 768  # Dummy embedding
    
    def _add_to_stm(self, data, embedding, context):
        # Simple FIFO with expiry for STM
        if len(self.stm) >= self.stm_capacity:
            # Remove oldest
            oldest_key = next(iter(self.stm))
            del self.stm[oldest_key]
        key = str(hash(data))
        self.stm[key] = {
            "data": data,
            "embedding": embedding,
            "context": context,
            "timestamp": time.time()
        }
    
    def _add_to_ltm(self, embedding, data, context):
        # Add to long-term memory (ChromaDB)
        self.ltm_collection.add(
            embeddings=[embedding],
            documents=[str(data)],
            metadatas=[{"context": context}]
        )
