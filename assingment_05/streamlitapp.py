import streamlit as st
import os
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="CSV SQL Chatbot")
st.title("CSV SQL Chatbot")

st.session_state.setdefault("show_preview", False)

#LLM
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

#Upload
file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    # Preview toggle
    if st.button("Toggle Data Preview"):
        st.session_state.show_preview = not st.session_state.show_preview

    if st.session_state.show_preview:
        st.dataframe(df.head())

    # Schema
    st.subheader("Schema")
    st.write(df.dtypes)

    #User Question
    question = st.text_input("Ask a question about this CSV")

    if question:
        prompt = f"""
        You are an expert SQL developer.
        Table name: data
        Schema: {df.dtypes}
        Question: {question}

        Write a valid SQLite SQL query only.
        If impossible, return "Error"
        """

        sql = llm.invoke(prompt).content.strip()

        st.subheader("Generated SQL")
        st.code(sql, language="sql")

        if sql.lower() != "error":
            try:
                result = sqldf(sql, {"data": df})
                st.subheader("Query Result")
                st.dataframe(result)

                explain_prompt = f"""
                Explain this result simply.

                Question: {question}
                Result:
                {result.head(10).to_string(index=False)}
                """

                explanation = llm.invoke(explain_prompt).content
                st.subheader("Explanation")
                st.write(explanation)

            except Exception as e:
                st.error("Error executing SQL")
                st.exception(e)
        else:
            st.error("LLM could not create SQL")
