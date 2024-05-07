from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
def process_upload(uploaded_file):
    sources_list = []
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
       file.write(uploaded_file.getvalue())
       file_name = uploaded_file.name

    loader = PyPDFLoader(temp_file)
    documents = loader.load()

 
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits = text_splitter.split_documents(documents)
    
    #create vectore store from embeddings
    faiss_index = FAISS.from_documents(all_splits, OpenAIEmbeddings())
    return faiss_index
    