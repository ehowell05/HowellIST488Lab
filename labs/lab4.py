import streamlit as st
from openai import OpenAI
import sys
import chromadb
from pathlib import Path
from PyPDF2 import PdfReader


__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

st.title("Lab 4 – RAG Vector DB Test")

if "openai_client" not in st.session_state:
    st.session_state.openai_client = OpenAI(api_key=st.secrets["EddieOpenAPIKey"])


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def add_to_collection(collection, text, filename):
    client = st.session_state.openai_client
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[filename],
        metadatas=[{"source": filename}]
    )


def initialize_vector_db():
    chroma_client = chromadb.PersistentClient(path="./ChromaDB_for_Lab")
    collection = chroma_client.get_or_create_collection("Lab4Collection")

    folder_path = "data/Lab-04-Data" 
    for file in Path(folder_path).glob("*.pdf"):
        text = extract_text_from_pdf(file)
        add_to_collection(collection, text, str(file.name))

    return collection


if "Lab4_VectorDB" not in st.session_state:
    st.session_state.Lab4_VectorDB = initialize_vector_db()


collection = st.session_state.Lab4_VectorDB


#testing
st.sidebar.header("Test Vector Search")
topic = st.sidebar.text_input("Enter a search term", placeholder="e.g., Generative AI")

if topic:
    client = st.session_state.openai_client

    response = client.embeddings.create(
        input=[topic],
        model="text-embedding-3-small"
    )

    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    st.subheader(f"Top 3 Results for '{topic}':")

    for i in range(len(results["ids"][0])):
        st.write(f"{i+1}. {results['ids'][0][i]}")

else:
    st.info("Enter a search term in the sidebar to test the Vector Database.")
