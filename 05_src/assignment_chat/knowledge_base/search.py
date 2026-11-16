from pathlib import Path
import chromadb
from langchain_core.tools import tool

# Store the vector database inside the assignment folder
DB_PATH = Path(__file__).resolve().parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="travel_knowledge",
    metadata={"hnsw:space": "cosine"}
)

# Small travel FAQ knowledge base
documents = [
    "For international travel, check your passport validity and visa requirements before booking.",
    "Travel insurance can help cover unexpected medical expenses, trip cancellations, and lost luggage.",
    "When booking flights, compare baggage allowances, cancellation policies, and layover times.",
    "A travel budget should include flights, accommodation, food, activities, and local transportation.",
    "For budget accommodation, compare hostels, guesthouses, and budget hotels.",
    "When travelling internationally, inform your bank and check foreign transaction fees.",
    "Pack essential medications, travel documents, chargers, and a small first-aid kit.",
    "Public transportation is often more affordable than taxis when exploring a new city.",
    "Check the local weather forecast before packing clothes and planning outdoor activities.",
    "Keep digital and printed copies of your passport, visa, and important travel documents."
]

if collection.count() == 0:
    collection.add(
        documents=documents,
        ids=[f"travel_{i}" for i in range(len(documents))]
    )


@tool
def search_travel_knowledge(query: str) -> str:
    """Search travel FAQs and retrieve information relevant to a travel question."""
    
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    matches = results["documents"][0]

    if not matches:
        return "I couldn't find relevant travel information."

    return "Here is some relevant travel information:\n" + "\n".join(
        f"- {item}" for item in matches
    )
