import streamlit as st

def display_thoughts(query):
    st.markdown("---")
    st.markdown(f"🧠 **Thoughts**: I retrieved context using embeddings for: *{query}*")
