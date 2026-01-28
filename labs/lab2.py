import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Lab 2")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
)
st.sidebar.title("Lab 2 Settings")
add_sum_sbox = st.sidebar.selectbox("Which kind of summary would you like to use?", ["in 100 Words", "in 2 Paragraphs", "in 5 Bullet Points"])
add_model_checkbox = st.checkbox("Would you like to use the stonger model?", value = False)
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets.EddieOpenAPIKey
#if not openai_api_key:
    #st.info("Please add your OpenAI API key to continue.", icon="🗝️")
#else:
def model_check(add_model_checkbox):
    if add_model_checkbox:
        model_check = "gpt-5-mini"
    else:
        model_check = "gpt-5-nano"


# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

try:
    client.models.list()
    st.success(f"API Key Success")
except Exception as e:
    st.error(f"API Key Failed: {e}")

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:

    # Process the uploaded file and question.
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {add_sum_sbox}",
        }
    ]

    # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
        model = model_check,
        messages=messages,
        stream=True,
    )
    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)