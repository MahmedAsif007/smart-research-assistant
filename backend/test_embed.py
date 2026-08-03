from langchain_ollama import OllamaEmbeddings
import os

embeddings = OllamaEmbeddings(
    model="gpt-oss:20b",
    base_url="https://ollama.com",
    client_kwargs={
        "headers": {
            "Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"
        }
    }
)

print(
    embeddings.embed_query("Hello world")
)