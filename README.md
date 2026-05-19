# 🧠 NL2SQL RAG Chatbot using Gemini + PostgreSQL

## 📌 Overview

This project is an AI-powered **Natural Language to SQL (NL2SQL)** system enhanced with **Retrieval-Augmented Generation (RAG)**. It converts natural language questions into SQL queries, executes them on a PostgreSQL database, and returns both structured results and natural language responses.

The system uses **Google Gemini (via LangChain)** for SQL generation and a **FAISS vector store** to retrieve similar few-shot examples, improving query accuracy and robustness.

---

## 🚀 Key Features

* Natural language to SQL conversion (NL2SQL)
* RAG-based few-shot learning for improved SQL generation
* FAISS vector database for semantic retrieval of examples
* Google Gemini LLM integration via LangChain
* Automatic PostgreSQL schema extraction
* Dynamic SQL execution and result handling
* Natural language explanation of query results
* Interactive Streamlit web interface

---

## 🏗️ System Workflow

1. User enters a natural language question
2. PostgreSQL schema is extracted automatically
3. FAISS retrieves relevant few-shot examples
4. Gemini generates SQL using schema + retrieved context
5. SQL query is executed on PostgreSQL
6. Results are returned as a DataFrame
7. Gemini converts results into a natural language response

---

## 🧰 Tech Stack

* Python
* Streamlit
* PostgreSQL
* SQLAlchemy
* LangChain
* Google Gemini API
* FAISS (Vector Search)
* HuggingFace Embeddings
* Pandas

---

## 📂 Project Structure

```id="2v7k6g"
nl2sql-rag-chatbot-gemini/
│
├── app.py
├── fewshots.json
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash id="l8v2cc"
git clone https://github.com/your-username/nl2sql-rag-chatbot-gemini.git
cd nl2sql-rag-chatbot-gemini
```

### 2. Create virtual environment

```bash id="v4g8jj"
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash id="r9p3aa"
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```id="k1s0pp"
GOOGLE_API_KEY=your_google_gemini_api_key
DB_URL=postgresql+psycopg2://username:password@host:port/dbname
```

---

### 5. Run the application

```bash id="m6t2zz"
streamlit run app.py
```

---

## 💡 Example Queries

* Show total revenue by month
* List top customers by spending
* How many orders were placed in 2024?
* Average order value per region

---

## 🧠 Technical Highlights

* FAISS-based semantic retrieval of few-shot SQL examples
* Embedding model: `all-MiniLM-L6-v2`
* Prompt augmentation using retrieved context
* Automatic conversion of non-PostgreSQL syntax
* Schema-aware SQL generation
* LLM-based natural language response generation

---

## 📌 Future Improvements

* Add SQL validation and safety layer
* Improve retrieval ranking (hybrid search)
* Support multiple database systems (MySQL, SQLite)
* Add query history and analytics dashboard
* Deploy using Docker and cloud database

---

## 👩‍💻 Author

**Dana Ahmed**
Computer Science Graduate
AI Engineer focused on NLP, LLM systems, and Computer Vision
