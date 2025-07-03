# enhanced_library_bot/app.py

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from tools.google_search import google_search
from tools.scholar_search import scholar_search
from tools.catalog_search import catalog_search
from tools.speech_module import recognize_speech, text_to_speech
from utils.thought_logger import display_thoughts
import os

st.set_page_config(page_title="Library AI Assistant", layout="wide")
st.title("📚 Library AI Assistant")

# Set API keys and environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="db", embedding_function=embedding)
llm = ChatOpenAI(temperature=0, model_name="gpt-4")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tools
tools = [
    Tool(name="Google Search", func=google_search, description="Searches Google for current info"),
    Tool(name="Scholar", func=scholar_search, description="Searches Google Scholar"),
    Tool(name="Catalog", func=catalog_search, description="Searches Library Catalog")
]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", memory=memory, verbose=True)

# Input options
input_mode = st.radio("Choose Input Mode", ["🧾 Text", "🎤 Voice"])
if input_mode == "🎤 Voice":
    query = recognize_speech()
    st.info(f"Recognized: {query}")
else:
    query = st.text_input("Ask me anything about the library, research, or resources:", "What are the library hours?")

# Response
if st.button("Submit") and query:
    retriever_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory)
    response = retriever_chain.run(query)
    st.markdown(f"### 🤖 Response:\n{response}")
    display_thoughts(query)
    text_to_speech(response)

# Show full memory
with st.expander("🧠 Conversation History"):
    for msg in memory.chat_memory.messages:
        st.markdown(f"**{msg.type.capitalize()}:** {msg.content}")
