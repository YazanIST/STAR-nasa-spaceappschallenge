from dotenv import load_dotenv
load_dotenv()

# VectorIndexRetriever
from llama_index.schema import NodeWithScore
from llama_index import GPTVectorStoreIndex, ServiceContext
from llama_index.storage import StorageContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.memory import ChatMemoryBuffer
from llama_index.embeddings import HuggingFaceEmbedding

import chromadb

chroma_client = chromadb.PersistentClient(path="distilbert/")

chroma_collection = chroma_client.get_or_create_collection("distilbert")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
embed_model = HuggingFaceEmbedding(model_name="distilbert-base-uncased")
service_context = ServiceContext.from_defaults(embed_model=embed_model)
index = GPTVectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context,
    service_context=service_context
)

memory = ChatMemoryBuffer.from_defaults(token_limit=1000)

chat_engine = index.as_chat_engine(
    similarity_top_k=5,
    chat_mode="context",
    memory=memory,
    system_prompt="You are an Artificial Intelligence (AI)-powered app called STAR " + \
                  "(Standards Technical Assistance Resource) that could " + \
                  "streamline the process and offer requirement " + \
                  "recommendations, you can be used as copilot, to help " + \
                  "mission designers blast off with even greater " + \
                  "confidence, knowing that they have the right " + \
                  "requirements in place. You should analyze and suggest " + \
                  "improvements to a NASA standards and recommend procedures."
)

# query_engine = index.as_query_engine()
retriever = index.as_retriever(
    similarity_top_k=5,
)

THRESHOLD = 1e-9

while True:
    q = input('User: ')
    if q == 'RESET':
        chat_engine.reset()
        continue

    response = chat_engine.chat(q)
    # top_k_similar_nodes = retriever.retrieve(q)
    top_k_similar_nodes = retriever.retrieve(str(response))
    to_view = []
    for node in top_k_similar_nodes:
        print(node.get_score(), end = ' ')
        if node.get_score() > THRESHOLD:
            to_view.append(node.metadata()['file_name'])
    print('STAR:', response)
    if len(to_view) > 0:
        print('References:')
        for i, filename in enumerate(to_view):
            splits = filename.split('_')
            page_number = int(splits[1])
            original_document = ''.join(splits[3:])
            print(f'\t{i + 1}- Document: {original_document[:-4]}, Page: {page_number}.')
