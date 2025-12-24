import chromadb

db = chromadb.PersistentClient(path="./my_chroma_db")

collection = db.get_or_create_collection(name="resume")

collection.add(
    ids=["resume_id"],
    embeddings=[[0.1, 0.2, 0.3]],  # list of vectors
    metadatas=[{
        "source": "resume.pdf",
        "page_count": 2
    }],
    documents=["gsdufgjj"]
)

print("total records:", collection.count())
