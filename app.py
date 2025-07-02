import streamlit as st
import json
from langchain_core.documents import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from tools import search_primo, search_google_scholar, search_libguides

# Load FAQ from JSON
with open("faq_chatbot_ready.json", "r") as f:
    faq_data = json.load(f)

docs = [Document(page_content=f"Q: {item['question']}\nA: {item['answer']}") for item in faq_data]

# Split, embed, and store documents
split_docs = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(docs)
from langchain.embeddings import OpenAIEmbeddings
embedding = OpenAIEmbeddings()

class SafeOpenAIEmbeddings(OpenAIEmbeddings):
    def embed_documents(self, texts):
        return embed_with_retry(self, input=texts, **self._invocation_params)

embedding = SafeOpenAIEmbeddings()
vectordb = FAISS.from_documents(split_docs, embedding)
qa_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0), retriever=vectordb.as_retriever())

# Agent setup for external tools
tools = [search_primo, search_google_scholar, search_libguides]
agent = initialize_agent(tools, ChatOpenAI(temperature=0), agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

# Streamlit UI
st.set_page_config(page_title="Ask LAIRA")
st.title("📚 Ask LAIRA - Library AI Chatbot")
query = st.text_input("Ask me a question:")

if query:
    if any(keyword in query.lower() for keyword in ["article", "find", "search"]):
        st.markdown(agent.run(query))
    else:
        st.markdown(qa_chain.run(query))
