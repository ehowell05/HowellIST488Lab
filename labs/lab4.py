import streamlit as st 
from openai import OpenAI
import sys 
import chromadb
from pathlib import Path 
from PyPDF2 import PdfReader


__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


chroma_client = chromadb.PersistentClient(path='./ChromaDB_for_Lab')
collection = chroma_client.get_or_create_collection('Lab4Collection')


if 'openai_client' not in st.session_state:
    st.session_state.openai_client = OpenAI(api_key=st.secrets.EddieOpenAPIKey)

def add_to_collection(collection, text, filename):
    client = st.session_state.openai_client
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    embedding = response.data[0].embedding
    collection.add(documents=[text], embeddings=[embedding], ids=[filename])

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def load_pdf_to_collection(folder_path, collection):
    for file in Path(folder_path).glob("*.pdf"):
        text = extract_text_from_pdf(file)
        add_to_collection(collection, text, str(file))


st.title("Lab 4: Chatbot Using RAG")

topic = st.sidebar.text_input('Topic', placeholder="Type your topic here...")

if topic:
    client = st.session_state.openai_client
    response = client.embeddings.create(input=[topic], model="text-embedding-3-small")

    query_embedding = response.data[0].embedding

    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    st.subheader(f"Rusults for '{topic}':")

    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        doc_id = results['ids'][0][i]

        st.write(f"**{i+1}. {doc_id}**")
else:
    st.info("Enter a topic in the sidebar to see relevant documents from the collection.")