from app.models.destination import Destination
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class VectorStoreService:
    def __init__(self, model_name: str = "all-minilm"):
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.vector_store = Chroma(
            embedding_function=self.embeddings, persist_directory="./chroma_db"
        )

    def add_destination(self, destination: Destination):
        self.vector_store.add_texts(
            texts=[destination.description],
            metadatas=[
                {
                    "id": destination.id,
                    "name": destination.name,
                    "country": destination.country,
                }
            ],
            ids=[destination.id],
        )

    def search_destinations(self, query: str, n_results: int = 5):
        return self.vector_store.similarity_search(query, k=n_results)


vector_store_service = VectorStoreService()
