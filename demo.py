import gradio as gr

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
                  "improvements to a NASA standards."
)
query_engine = index.as_query_engine()
retriever = index.as_retriever(
    similarity_top_k=5,
)

THRESHOLD = 1e-9

def inference(text, reset):
    if text:
        response = chat_engine.chat(text)
        top_k_similar_nodes = retriever.retrieve(text)
        to_view = []
        for node in top_k_similar_nodes:
            # print(node.get_score(), end = ' ')
            if node.get_score() > THRESHOLD:
                to_view.append((node.metadata()['file_name'], node.get_score()))
            # to_view.append((node.metadata()['file_name'], node.get_score()))
        references = ""
        if len(to_view) > 0:
            for i, t in enumerate(to_view):
                filename, score = t
                splits = filename.split('_')
                page_number = int(splits[1])
                original_document = ''.join(splits[3:])
                references += f'{i + 1}- Document: ' + \
                    f'{original_document[:-4]}, Page: ' + \
                        f'{page_number} (Score: {score}).'
                if i != len(to_view) - 1:
                    references += '\n'
        if reset:
            memory.reset()
        return response, references
    elif reset:
        memory.reset()
    return "", ""

examples = [
    [
        "How should the length-to-depth ratio of the initial flaw be " + \
        "assumed when using the NASGRO® computer program for glass " + \
        "structure analysis? Please provide a detailed procedure.",
        True
    ]
]

playground = gr.Interface(
    fn=inference,
    inputs=[
        gr.Textbox(
            value="Hello, who are you?",
            label="Input",
            info="Chat with STAR."
        ),
        gr.Checkbox(
            label="Reset chat history",
            info="Start a new conversation from scratch with STAR."
        )
    ],
    outputs=[
        gr.Textbox(
            label="Response"
        ),
        gr.Textbox(
            label="References"
        )
    ],
    examples=examples,
    cache_examples=True,
    allow_flagging=False
)

playground.launch(share=True)
