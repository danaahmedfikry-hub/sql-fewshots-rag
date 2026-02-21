import os
import json
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DB_URL = os.getenv("DB_URL")

llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="SQL Chatbot")
st.title("Chat with Postgres DB")

@st.cache_resource
def get_engine():
    return create_engine(DB_URL)

def get_schema():
    engine = get_engine()
    
    inspector_query = text("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    schema_str = ""
    try:
        with engine.connect() as conn:
            result = conn.execute(inspector_query)
            current_table = ""
            for row in result:
                table_name, column_name = row[0], row[1]
                if table_name != current_table:
                    schema_str += f"\nTable: {table_name}\nColumns: "
                    current_table = table_name
                schema_str += f"{column_name}, "
    except Exception as e:
        st.error(f"Error reading schema: {e}")
        
    return schema_str

def get_date_like_columns():
    engine = get_engine()
    query = text("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema='public'
          AND (column_name ILIKE '%date%' OR column_name ILIKE '%time%');
    """)
    date_cols = {}
    with engine.connect() as conn:
        for row in conn.execute(query):
            table, column = row[0], row[1]
            date_cols.setdefault(table, []).append(column)
    return date_cols

date_columns = get_date_like_columns()

def execute_sql(query):
    engine = get_engine()
    try:
        for table, cols in date_columns.items():
            for col in cols:
                if "EXTRACT" in query.upper() or "YEAR" in query.upper():
                    query = query.replace(f'"{col}"', f'TO_DATE("{col}", \'YYYY-MM-DD\')')
        with engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df
    except Exception as e:
        st.error(f"Error executing SQL: {e}")
        return pd.DataFrame()

vectorstore = None
retriever = None

def load_fewshots_vectorstore(fewshot_path="D:\\Downloads\\fewshots.json"):
    global vectorstore, retriever
    if vectorstore is None:
        with open(fewshot_path, "r", encoding="utf-8") as f:
            fewshots = json.load(f)
        docs = []
        for ex in fewshots:
            content = f"Q: {ex['naturalQuestion']}\nSQL: {ex['sqlQuery']}"
            docs.append(content)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_texts(docs, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever

def get_sql_from_gemeni(question, schema):
    retriever_local = load_fewshots_vectorstore()
    retrieved_docs = retriever_local.invoke(question) 
    fewshot_context = "\n".join([doc.page_content for doc in retrieved_docs])
    prompt = f"""
    You are an expert Postgres SQL Data Analyst.
    Here is the database schema:
    {schema}

    Here are some example questions and SQL queries for guidance (they may use non-PostgreSQL SQL):
    {fewshot_context}

    Your task is to write a SQL query in **valid PostgreSQL syntax** that answers the following question:
    {question}

    Guidelines:
    - Always use double quotes around any table or column names that are not all lowercase.
    - Always use double quotes around any table or column names exactly as they appear in the schema.
    - If the examples use non-PostgreSQL syntax (like `||` for concatenation), convert it to proper PostgreSQL SQL.
    - Return only the SQL query, without any explanation or comments.
    - Make sure the query runs in PostgreSQL without errors.
    """
    response = llm.invoke(prompt)
    clean_sql = response.content.replace("```sql", "").replace("```", "").strip()
    return clean_sql

def get_natural_response(question, data):
    prompt = f"""
    User Question: {question}
    Data returned from SQL query: {data}

    Task: Answer the user's question based on the data returned from the SQL query.
    
    - Always wrap table and column names in double quotes if they are not all lowercase.
    - If the SQL query returns no rows, respond:"No results match the criteria."
    - Do not modify column or table names yourself in Python.
    - Make sure the query runs directly in PostgreSQL without errors.
    
    """
    response = llm.invoke(prompt)
    return response.text.strip()

question = st.text_input("Ask a question about your database:")
if question:
    schema = get_schema()
    sql_query = get_sql_from_gemeni(question, schema)
    st.subheader("🔎 Generated SQL Query")
    st.code(sql_query, language="sql")
    
    data = execute_sql(sql_query)
    st.subheader("📊 Query Result")
    st.dataframe(data)
    
    answer = get_natural_response(question, data)
    st.write(answer)