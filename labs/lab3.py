import streamlit as st
from openai import OpenAI

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

system_prompt = {"role": "system", "content": "You are a helpful assistant. Explain answers so a 10-year-old can understand."}
client = OpenAI(api_key=st.secrets.EddieOpenAPIKey)

user_input = st.text_input("Ask me anything:")

if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})

    buffer_messages = [system_prompt] + st.session_state['messages'][-4:]

    response = client.chat.completions.create(
        model="gpt-5",
        messages=buffer_messages
    )
    bot_reply = response.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": bot_reply})

for msg in st.session_state['messages']:
    st.chat_message(msg['role']).markdown(msg['content'])

if st.session_state['messages'] and st.session_state['messages'][-1]['role'] == 'assistant':
    more = st.radio("Do you want more info?", ["Yes", "No"], key="more_info_radio")
    if more == "Yes":
        buffer_messages = [system_prompt] + st.session_state['messages'][-4:]
        response = client.chat.completions.create(
            model="gpt-5",
            messages=buffer_messages + [{"role": "user", "content": "Please give more details"}]
        )
        st.session_state['messages'].append({"role": "assistant", "content": response.choices[0].message.content})
