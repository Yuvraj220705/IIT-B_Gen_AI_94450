import os
import chromadb
from datetime import date
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
from langchain.agents import create_agent

# --------------------- ENV + MODEL ---------------------
load_dotenv()

model = init_chat_model(
    model="moonshotai/kimi-k2-instruct-0905",
    api_key=os.getenv("GROQ_API_key"),
    base_url="https://api.groq.com/openai/v1",
    model_provider="openai"
)

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5@q8_0",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="demo",
    check_embedding_ctx_length=False
)

# --------------------- CHROMA SETUP ---------------------
db = chromadb.PersistentClient(path="./Resume_base")
collection = db.get_or_create_collection("resume")


def add_data(data, metadata, embed, id):
    try:
        collection.add(
            ids=id,
            embeddings=embed,
            metadatas=metadata,
            documents=data
        )
    except Exception:
        print("Failed to add data")


def delete_data(id):
    try:
        collection.delete(ids=[id])
        print(f"Deleted {id}")
    except Exception:
        print("Failed to delete")


def update_data(data, metadata, embed, id):
    delete_data(id)
    add_data(data=data, metadata=metadata, embed=embed, id=id)


def get_data_for_query(Equery):
    return collection.query(query_embeddings=Equery, n_results=3)

# --------------------- EMBEDDING + PDF ---------------------


def get_name(path):
    last = path.split("\\")[-1]
    id_part = last.split(".pdf")[0]
    final_id = f"{id_part}_{date.today()}"
    return last, final_id


def add_pdf(path):
    name, id = get_name(path)
    loader = PyPDFLoader(path)
    docs = loader.load()

    content = "".join([d.page_content for d in docs])

    metadata = {
        "source": path,
        "File_name": name,
        "Pages": len(docs)
    }

    embed_data = embed_model.embed_documents([content])
    add_data(data=content, metadata=metadata, embed=embed_data, id=id)


def update_pdf(id, path):
    try:
        name, new_id = get_name(path)
        loader = PyPDFLoader(path)
        docs = loader.load()

        content = "".join([d.page_content for d in docs])

        metadata = {
            "source": path,
            "File_name": name,
            "Pages": len(docs)
        }

        embed_data = embed_model.embed_documents([content])
        update_data(data=content, metadata=metadata, embed=embed_data, id=f"New_{new_id}")
    except Exception:
        return "Failed to update the data"


def read_query(query):
    Equery = embed_model.embed_documents([query])
    result = get_data_for_query(Equery)
    return result if result else None

# --------------------- TOOL ---------------------


@tool
def update_file(ids, path):
    """
    Updates an existing resume in Chroma DB.
    Use ONLY when user explicitly wants to update/modify a file.
    """
    print("Tool update_file called")
    return update_pdf(ids, path)

# --------------------- AGENT ---------------------
agent = create_agent(
    model=model,
    tools=[update_file],
    system_prompt="""
You are an AI agent with tool abilities.
Use provided context if useful.
Use tools only when required.
Return only the final answer in plain text.
"""
)

conversation = []


def call_model(query, data, metadata):
    payload = f"context data = {data}, metadata = {metadata}, user query = {query}"

    temp = conversation.copy()
    temp.append({"role": "user", "content": payload})

    output = agent.invoke({"messages": temp})
    result = output["messages"][-1].content

    conversation.append({"role": "user", "content": query})
    conversation.append({"role": "assistant", "content": result})

    return result


if __name__ == "__main__":
    print(call_model("What is your name?", "Assistant test context", "sample.pdf"))
