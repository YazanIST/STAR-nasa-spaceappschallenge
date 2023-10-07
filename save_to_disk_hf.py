from dotenv import load_dotenv
load_dotenv()

from llama_index import VectorStoreIndex, SimpleDirectoryReader, LangchainEmbedding, ServiceContext
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.storage import StorageContext
from llama_index.vector_stores import ChromaVectorStore

import chromadb

import transformers

from langchain.embeddings.huggingface import HuggingFaceEmbeddings

chroma_client = chromadb.PersistentClient(path="chroma_db/")

chroma_collection = chroma_client.get_or_create_collection("nasa_data")

documents = SimpleDirectoryReader('pages').load_data()

print('Pages are loaded.')

# Load the Hugging Face embedding model

# embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
# embed_model = transformers.AutoModel.from_pretrained("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

print('Model is loaded into GPU.')

# Create a LangchainEmbedding object
# langchain_embedding = LangchainEmbedding(embed_model)

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# Create a storage context with the LangchainEmbedding object
storage_context = StorageContext.from_defaults(vector_store=vector_store)

print('Will start indexing and embedding.')

service_context = ServiceContext.from_defaults(embed_model=embed_model)

# Create a VectorStoreIndex object with the LangchainEmbedding object
# index = VectorStoreIndex.from_documents(
#     documents,
#     storage_context=storage_context,
#     chroma_collection=chroma_collection,
#     show_progress=True,
#     embed_model=embed_model,
#     service_context=service_context
# )
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    chroma_collection=chroma_collection,
    show_progress=True,
    service_context=service_context
)
