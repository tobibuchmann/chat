"""

This module uses Streamlit to create an interactive web application for a chatbot with various features.

The application interface is organized into three rows:
    1. The first row contains a Chatbot component that simulates a conversation with a language model, along with a hidden
    reference bar initially. The reference bar can be toggled using a button.

    2. The second row consists of a Textbox for user input. Users can enter text or upload PDF/doc files.

    3. The third row includes buttons for submitting text, toggling the reference bar visibility, uploading PDF/doc files,
    adjusting temperature for GPT responses, selecting the document type, and clearing the input.

    The application processes user interactions:
    - Uploaded files trigger the processing of the files, updating the input and chatbot components.
    - Submitting text triggers the chatbot to respond, considering the selected document type and temperature settings.
    The response is displayed in the Textbox and Chatbot components, and the reference bar may be updated.

    The application can be run as a standalone script, launching the Gradio interface for users to interact with the chatbot.

    Note: The docstring provides an overview of the module's purpose and functionality, but detailed comments within the code
    explain specific components, interactions, and logic throughout the implementation.

"""
# Environment: streamlit


import streamlit as st
from streamlit_chat import message


from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import tempfile
from operator import itemgetter
from typing import List

from st_paywall import add_auth


from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

import os



from utils.create_chain import create_conversational_chain
from utils.process_upload import process_upload


add_auth(required=True)


################## Define functions

def initialize_session_state():
    # session state is an object and history is reated here as a key; allways, first check if the key is present in the session state
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask a question about your files."]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hi"]


def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def display_chat_history(chain):
    reply_container = st.container(height=500)
    question_container = st.container()

    with question_container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about your Documents", key='input')
            submit_button = st.form_submit_button(label='Send')
            # Button to toggle sidebar visibility
           

        if submit_button and user_input:
            with st.spinner('Generating response...'):
                output = conversation_chat(user_input, chain, st.session_state['history'])

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

    



########################### Main


initialize_session_state()

st.set_page_config(layout="wide", page_title="Paper chat app")


st.title ("SYS-MAT Chatbot: Ask me anything about your perovskite files!")

uploaded_file = st.file_uploader("Choose a PDF file", type = "pdf")

if uploaded_file:
    st.write("File uploaded successfully!")
    faiss_index = process_upload(uploaded_file)
    # Create the chain object
    chain = create_conversational_chain(faiss_index)
    display_chat_history(chain)
else:
    st.write("Please upload a PDF file to start the chatbot.")

