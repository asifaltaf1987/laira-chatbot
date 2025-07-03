# enhanced_library_bot/app.py

import streamlit as st
from PIL import Image
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from tools.google_search import google_search
from tools.scholar_search import scholar_search
from tools.catalog_search import catalog_search
from tools.speech_module import recognize_speech, text_to_speech
from utils.thought_logger import display_thoughts
from tools.web_scraper import web_scrape_summary
from langchain.docstore.document import Document
import os

st.set_page_config(page_title="Laira", layout="wide")

# Header Avatar and Greeting
col1, col2 = st.columns([1, 8])
with col1:
    avatar = Image.open("static/avatar.png")  # Place avatar image at /static/avatar.png
    st.image(avatar, width=75)
with col2:
    st.markdown("## Laira")
    st.markdown("Hello! I am Laira, an AI assistant at RCSI Bahrain Library. How can I help you today?")

# Predefined Quick Buttons
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

# API keys and vector setup
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
embedding = OpenAIEmbeddings()
docs = [Document(page_content="Welcome to the library FAQ chatbot")]
vectorstore = FAISS.from_documents(docs, embedding)
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-4")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tools
tools = [
    Tool(name="Google Search", func=lambda q: google_search(q, st.session_state.get("search_mode", "library")), description="Searches Google"),
    Tool(name="Scholar", func=scholar_search, description="Searches Google Scholar"),
    Tool(name="Catalog", func=catalog_search, description="Searches Library Catalog"),
    Tool(name="Web Scraper", func=web_scrape_summary, description="Scrapes public websites for current info")
]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", memory=memory, verbose=True)

# Input
input_mode = st.radio("Choose Input Mode", ["🧾 Text", "🎤 Voice"])
query = st.session_state.get("query", "")
if input_mode == "🎤 Voice":
    query = recognize_speech()
    st.info(f"Recognized: {query}")
else:
    query = st.text_input("Ask me anything about the library, research, or resources:", value=query)

# Response logic
if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        retriever_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)
        response = retriever_chain.run(query)
        used_tool = "RAG Vector Retrieval"

        if any(k in query.lower() for k in ["book", "article", "journal", "ebook", "find in library", "full text", "textbook"]):
            response = catalog_search(query)
            used_tool = "Catalog"
        elif any(k in query.lower() for k in ["scholar", "research", "citation"]):
            response = scholar_search(query)
            used_tool = "Google Scholar"
        elif any(p in response.lower() for p in ["i don't have", "no relevant", "not sure", "sorry", "don't know", "cannot help"]):
            response = google_search(query, mode="global")
            used_tool = "Google Search"
        else:
            response = web_scrape_summary(query)
            used_tool = "Web Scraper"

    st.markdown(f"### 🤖 Response:\n{response}")
    display_thoughts(query, tool_used=used_tool)
    text_to_speech(response)

# Memory Display
with st.expander("🧠 Conversation History"):
    for msg in memory.chat_memory.messages:
        st.markdown(f"**{msg.type.capitalize()}:** {msg.content}")
