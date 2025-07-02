import streamlit as st
import pandas as pd
import json

from langchain_core.documents import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, AgentType

from tools import search_primo, search_google_scholar, search_libguides

# Load FAQ from JSON
with open("faq_chatbot_ready.json", "r") as f:
    faq_data = json.load(f)

# Convert FAQ into documents
docs = [Document(page_content=f"Q: {item['question']}\nA: {item['answer']}") for item in faq_data]

# Split, embed, and store documents
split_docs = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(docs)
embedding = OpenAIEmbeddings()
vectordb = FAISS.from_documents(split_docs, embedding)
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
