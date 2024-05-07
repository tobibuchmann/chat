import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain.chains import ConversationalRetrievalChain

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from utils.create_chain import create_conversational_chain
from utils.process_upload import process_upload

from PIL import Image
# Loading Image using PIL
im = Image.open('logo.png')


load_dotenv()



if "chat_history" not in st.session_state:
    st.session_state.chat_history = []




st.set_page_config(page_title="ChatifyDocs", page_icon=im, layout="wide")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


# Display your logo
st.image('logo.png', width=200)
#st.title("Chat app")


uploaded_file = st.file_uploader("Choose a PDF file", type = "pdf")






# get reponse

def get_response(query, chat_history):
    template = """
        You are a helpful assistant. Answer the following questions considering the history of the conversation:    

        Chat history: {chat_history}

        User query: {question}
        """


    prompt = ChatPromptTemplate.from_template(template)

    #llm = ChatOpenAI()

    #chain = prompt | llm | StrOutputParser()

    chain = create_conversational_chain(faiss_index)
    output_parser = StrOutputParser()  # Create an instance of StrOutputParser

    responses = chain.stream({
        "chat_history": chat_history,
        "question": query

    })
    # Process the responses to extract the 'answer'
    answer_responses = [response['answer'] for response in responses if 'answer' in response]

    return answer_responses

if uploaded_file:
    st.write("File uploaded successfully!")
    faiss_index = process_upload(uploaded_file)
    # Create the chain object

    # convesation

    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)


# user input
    user_query = st.chat_input("Enter your question.", key="user_query")

    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))

        st.session_state.chat_history.append(AIMessage(ai_response))
    
else:
    st.write("Please upload a PDF file to start the chatbot.")





# Define your footer content

#def footer():
#    st.sidebar.markdown(
#        """
#        [Your Footer Link Text](#) | Other Footer Links
#        """,
#        unsafe_allow_html=True
#    )

# Call the footer function at the end of your Streamlit app
#footer()




