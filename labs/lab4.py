import streamlit as st
from openai import OpenAI
import chromadb
from pathlib import Path
from PyPDF2 import PdfReader

#Coding Localy
#__import__('pysqlite3')
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

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

part_1 = '''
#Part A Testing
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
'''

#Part B
st.sidebar.header("Test Vector Search")
topic = st.sidebar.text_input("Enter a question", placeholder="e.g., What is the grading rubric for IST 256?")

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

    retrieved_docs = results["documents"][0]
    retrieved_ids = results["ids"][0]

    context = ""
    for i in range(len(retrieved_docs)):
        context = context + "\n\nSource: " + retrieved_ids[i] + "\n" + retrieved_docs[i] #ChatGPT helped me with this part, I had trouble formatting the retrieved documents to contain the most context.

    prompt = f'''You are an course assistant chatbot. 
    Use the following documentation as your base knowledge for your answers. 
    If your answer is based of a specific document, please cite the source in your answer in a clear manner for example "IST 256 - Grading Rubric".
    If the documents do not contain any relevant information, please say "I don't know".
    Documentation:
    {context}

    Question: {topic}
    '''

    response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": prompt}]
)

    st.write(response.choices[0].message.content)


else:
    st.info("Enter a search term in the sidebar to test the Vector Database.")