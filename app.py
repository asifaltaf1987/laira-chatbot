# laira/app.py

import streamlit as st
from PIL import Image
import os
from langdetect import detect

from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from tools.google_search import google_search
from tools.scholar_search import scholar_search
from tools.catalog_search import catalog_search
from tools.speech_module import text_to_speech
from tools.web_scraper import web_scrape_summary
from utils.thought_logger import display_thoughts

# Page config
st.set_page_config(page_title="Laira", layout="wide")

# Header with avatar
col1, col2 = st.columns([1, 8])
with col1:
    avatar_path = "static/avatar.png"
    if os.path.exists(avatar_path):
        avatar = Image.open(avatar_path)
        st.image(avatar, width=75)
    else:
        st.warning("⚠️ Avatar not found.")
with col2:
    st.markdown("## Laira")
    st.markdown("Hi! I'm Laira, your multilingual digital library assistant at RCSI Bahrain Library. Ask me anything about research, resources, or services — in any language you prefer!")

# Quick question buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Help me find an article"):
        st.session_state.query = "Help me find an article"
with col2:
    if st.button("Library hours"):
        st.session_state.query = "What are the library hours?"
with col3:
    if st.button("Study rooms"):
        st.session_state.query = "How do I book a study room?"

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("Evaluate a source"):
        st.session_state.query = "How do I evaluate a scholarly source?"
with col5:
    if st.button("I can't access a resource"):
        st.session_state.query = "I can't access a resource"
with col6:
    if st.button("Community members"):
        st.session_state.query = "Who can use library services?"

# OpenAI setup
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
embedding = OpenAIEmbeddings()

# RCSI website sources for live scraping
urls = [
    "https://rcsi-mub.alma.exlibrisgroup.com/discovery/search?vid=968RCSI_INST:968RCSI",
    "https://www.rcsi.com/bahrain/library",
    "https://libguides.rcsi-mub.com",
    "https://libguides.rcsi-mub.com/az.php",
    "https://rcsi-bh.libcal.com/reserve/studyrooms",
    "https://libguides.rcsi-mub.com/appointments",
    "https://libguides.rcsi-mub.com/faq",
    "https://libguides.rcsi-mub.com/researchvideos"
]

# Load, chunk, and embed live documents
loader = WebBaseLoader(urls)
raw_docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = splitter.split_documents(raw_docs)
vectorstore = FAISS.from_documents(docs, embedding)

# Build memory + retrieval QA
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
retrieval_chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4"), retriever=vectorstore.as_retriever())

# System prompt
system_prompt = (
    "You are LAIRA, a friendly and helpful multilingual AI assistant at RCSI Bahrain Library. "
    "Answer in the same language as the question. Provide clickable links, ask clarifying questions when needed, "
    "and say 'I don't know' if unsure. Stay in your librarian persona."
)

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0,
    model_name="gpt-4"
)

tools = [
    Tool(name="Library Knowledge Base", func=retrieval_chain.run, description="Answers using RCSI Bahrain library website content"),
    Tool(name="Google Search", func=lambda q: google_search(q, st.session_state.get("search_mode", "library")), description="Searches Google"),
    Tool(name="Scholar", func=scholar_search, description="Searches Google Scholar"),
    Tool(name="Catalog", func=catalog_search, description="Searches Library Catalog"),
    Tool(name="Web Scraper", func=web_scrape_summary, description="Scrapes websites for current info")
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", memory=memory, verbose=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Render conversation
st.markdown("## 💬 Chat with Laira")
for sender, message in st.session_state.chat_history:
    with st.container():
        if sender == "user":
            st.markdown(
                f"""
                <div style='background-color:#f1f3f6;padding:12px;border-radius:10px;margin:10px 0;display:flex;align-items:center;'>
                    <img src="https://img.icons8.com/ios-filled/50/000000/user.png" width="32" style="margin-right:10px;">
                    <div><strong>You:</strong><br>{message}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='background-color:#e8f0fe;padding:12px;border-radius:10px;margin:10px 0;display:flex;align-items:center;'>
                    <img src="static/avatar.png" width="32" style="border-radius:50%;margin-right:10px;">
                    <div><strong>Laira:</strong><br>{message}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Input field
with st.form(key="chat_input_form", clear_on_submit=True):
    user_input = st.text_input("Ask me anything!", placeholder="Ask me anything about the library...")
    submitted = st.form_submit_button("➔")

if submitted and user_input:
    with st.spinner("Thinking..."):
        result = agent.run(user_input)
        response = result.get("output", str(result)) if isinstance(result, dict) else str(result)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response))
        display_thoughts(user_input, tool_used="Agent")

# Auto-submit if button query was triggered
if "query" in st.session_state and st.session_state.query:
    user_input = st.session_state.query
    st.session_state.query = ""
    submitted = True
