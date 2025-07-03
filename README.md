# LAIRA Chatbot

**LAIRA** (Library AI Research Assistant) is a conversational AI chatbot designed for the RCSI Bahrain Library. LAIRA answers library-related FAQs, searches your Primo catalog, queries LibGuides, explores your library website, and verifies scholarly topics using Google Scholar. Built with LangChain, Streamlit, ChromaDB, and OpenAI, it now includes support for Google Search, voice interaction, and modular LangChain tools for future flexibility. It runs entirely via GitHub and Streamlit Cloud—no local installation needed.

---

## 🔧 Features

- Search and summarize academic articles using RCSI Primo  
- Query Google Scholar and LibGuides with follow-up suggestions  
- Answer FAQs using embedded knowledge (vector RAG)  
- Google Search integration (via tool agent)  
- Voice input and output (speech-to-text and TTS)  
- Conversational memory for contextual awareness  
- Intelligent multi-step reasoning with LangChain Agents  
- Modular codebase with externalized tools and utilities  
- Ready-to-deploy via Streamlit Cloud  

---

## 🔗 Live Resources (Integrated)

- 🔎 [RCSI Primo](https://rcsibahrain.primo.exlibrisgroup.com/discovery/search?vid=973RCSIB_INST:RCSIB&lang=en)  
- 🏛 [Library Homepage](https://www.rcsi.com/bahrain/library)  
- 📚 [LibGuides](https://library.rcsi-mub.com/library/library-guides)  
- 📂 [Database A-Z List](https://library.rcsi-mub.com/az/databases)  
- 📅 [Study Room Booking](https://lrcroombookings.rcsi-mub.com/)  
- 👩‍🏫 [Librarian Appointments](https://lrcroombookings.rcsi-mub.com/appointments/)  
- ❓ [Library FAQs](https://libchat.rcsi-mub.com/)  
- 🎥 [Research Skills Videos](https://library.rcsi-mub.com/c.php?g=1284683&p=10624448)  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/laira-chatbot.git
cd laira-chatbot
```

### 2. File Structure

- `app.py` – Main Streamlit app  
- `tools/` – Modular LangChain tools (Google, Scholar, Catalog, Voice)  
- `utils/` – Thought explanation utility  
- `faq_chatbot_ready.csv` – FAQ dataset  
- `requirements.txt` – Required packages  

### 3. Requirements

```txt
openai
langchain
chromadb
streamlit
tiktoken
pandas
beautifulsoup4
requests
gTTS
SpeechRecognition
pyaudio
```

---

## 🧠 Usage

### Add Your OpenAI Key

In Streamlit Cloud secrets or locally:

```bash
export OPENAI_API_KEY=your-key-here
```

### Run Locally (optional)

```bash
streamlit run app.py
```

### Deploy on Streamlit Cloud

1. Push repo to GitHub  
2. Go to https://streamlit.io/cloud  
3. Connect repo, set `app.py` as main file  
4. Add secret: `OPENAI_API_KEY=sk-...`  

---

## 💬 Example Interactions

**User:** _Help me find an article on nanomedicine_  
**LAIRA:** Searches Primo → Displays top articles + follow-up in Scholar  

**User:** _Explain nanomedicine in cancer treatment_  
**LAIRA:** Summary generated via LLM + links to deeper reading  

**User:** _Search recent medical AI news_  
**LAIRA:** Google search triggered with latest links displayed  

---

## 🔮 Future Enhancements

- Full Google Search API or SERP tool integration  
- Long-term memory (persistent user context)  
- Automated FAQ updates from LibGuides and LibAnswers  
- Integration with live chat or WhatsApp  
- Enhanced analytics and usage dashboard  

---

## 🤝 Acknowledgements

- RCSI Bahrain Library  
- Powered by [LangChain](https://www.langchain.com/), [Streamlit](https://streamlit.io/), [OpenAI](https://platform.openai.com/)  

---

## 📜 License

Use responsibly and in compliance with OpenAI’s terms.
