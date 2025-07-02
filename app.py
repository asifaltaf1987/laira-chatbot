import streamlit as st
import pandas as pd
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from tools import search_primo, search_google_scholar, search_libguides

# Load FAQ
df = pd.read_csv("faq_chatbot_ready.csv")
docs = [Document(page_content=f"Q: {row['question']}\nA: {row['answer']}") for _, row in df.iterrows()]
split_docs = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(docs)
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(split_docs, embedding, persist_directory="faq_db")
qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(), retriever=vectordb.as_retriever())

# Agent setup
tools = [search_primo, search_google_scholar, search_libguides]
agent = initialize_agent(tools, ChatOpenAI(), agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

# Streamlit UI
st.set_page_config(page_title="Ask LAIRA")
st.title("📚 Ask LAIRA - Library AI Chatbot")
query = st.text_input("Ask me a question:")

if query:
    if any(keyword in query.lower() for keyword in ["article", "find", "search"]):
        st.markdown(agent.run(query))
    else:
        st.markdown(qa_chain.run(query))