import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("Lab 2")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
)
st.sidebar.title("Lab 2 Settings")
add_sum_sbox = st.sidebar.selectbox("Which kind of summary would you like to use?", ["in 100 Words", "in 2 Paragraphs", "in 5 Bullet Points"])
add_model_checkbox = st.sidebar.checkbox("Would you like to use the stonger model?", value = False)



def model_check(add_model_checkbox):
    if add_model_checkbox:
        model_check = "gpt-5-mini"
    else:
        model_check = "gpt-5-nano"
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets.EddieOpenAPIKey

client = OpenAI(api_key=openai_api_key)

try:
    client.models.list()
    st.success(f"API Key Success")
except Exception as e:
    st.error(f"API Key Failed: {e}")

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .pdf])", type=("txt", "pdf")
)

if uploaded_file:

    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        document = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        document = uploaded_file.read().decode("utf-8")

    response = client.responses.create(
        model=model_check(add_model_checkbox),
        input=f"Here is a document:\n{document}\n\nQuestion: {add_sum_sbox}",
        stream=True,
    )

    def stream_text():
        for event in response:
            if event.type == "response.output_text.delta":
                yield event.delta

    st.write_stream(stream_text())