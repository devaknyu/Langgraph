import streamlit as st
from langchain_core.messages import HumanMessage
from ChatBot_backend import chatbot

CONFIG = {"configurable": {"thread_id": "thread-1"}}
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

for messages in st.session_state['chat_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])
# chat_history: {"role": 'user' or 'assistent', 'content': ".."}

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)
    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response['messages'][-1].content
    st.session_state['chat_history'].append({"role":"assistant", "content": ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)                              
    
