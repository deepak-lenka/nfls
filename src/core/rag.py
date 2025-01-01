from typing import List, Dict
import chromadb
from chromadb.config import Settings
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGSystem:
    """Retrieval-Augmented Generation system for NFL analysis"""
    
    def __init__(self, collection_name: str = "nfl_data"):
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="data/chroma_db"
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize sentence transformer
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store"""
        # Extract text and metadata
        texts = [doc['text'] for doc in documents]
        ids = [str(i) for i in range(len(documents))]
        metadatas = [doc.get('metadata', {}) for doc in documents]
        
        # Generate embeddings
        embeddings = self.model.encode(texts).tolist()
        
        # Add to collection
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
    def query(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """Query the vector store"""
        # Generate query embedding
        query_embedding = self.model.encode(query_text).tolist()
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
            
        return formatted_results
        
    def update_document(self, doc_id: str, new_text: str, metadata: Dict = None):
        """Update a document in the vector store"""
        # Generate new embedding
        new_embedding = self.model.encode(new_text).tolist()
        
        # Update document
        self.collection.update(
            ids=[doc_id],
            embeddings=[new_embedding],
            documents=[new_text],
            metadatas=[metadata] if metadata else None
        )
        
    def delete_documents(self, doc_ids: List[str]):
        """Delete documents from the vector store"""
        self.collection.delete(ids=doc_ids)
        
    def get_similar_documents(self, doc_id: str, n_results: int = 5) -> List[Dict]:
        """Find documents similar to a given document"""
        # Get document
        doc = self.collection.get(ids=[doc_id])
        if not doc['embeddings']:
            return []
            
        # Query using document's embedding
        results = self.collection.query(
            query_embeddings=[doc['embeddings'][0]],
            n_results=n_results + 1  # Add 1 to account for the query document
        )
        
        # Format results, excluding the query document
        formatted_results = []
        for i in range(len(results['documents'][0])):
            if results['ids'][0][i] != doc_id:
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
                
        return formatted_results
