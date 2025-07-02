# LAIRA Chatbot

**LAIRA** (Library AI Research Assistant) is a conversational AI chatbot designed for the RCSI Bahrain Library. LAIRA answers library-related FAQs, searches your Primo catalog, queries LibGuides, explores your library website, and verifies scholarly topics using Google Scholar. Built with LangChain, Streamlit, ChromaDB, and OpenAI, it runs entirely via GitHub and Streamlit Cloud, no local installation needed.

---

## 🔧 Features

- Search and summarize academic articles using RCSI Primo
- Query Google Scholar and LibGuides with follow-up suggestions
- Answer FAQs using embedded knowledge
- Intelligent multi-step reasoning with LangChain Agents
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
- `tools.py` – LangChain Tools (Primo, Scholar, LibGuides)
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

---

## 🔮 Future Enhancements

- Full Google Search API or SERP tool integration
- LangChain memory for multi-turn conversations
- Weekly crawler sync from LibGuides
- Personalized suggestions based on query logs

---

## 🤝 Acknowledgements

- RCSI Bahrain Library
- Powered by [LangChain](https://www.langchain.com/), [Streamlit](https://streamlit.io/), [OpenAI](https://platform.openai.com/)

---

## 📜 License

Use responsibly and in compliance with OpenAI’s terms.