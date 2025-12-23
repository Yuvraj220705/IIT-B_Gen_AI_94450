import streamlit as st
import os
import pandas as pd
from pandasql import sqldf
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

st.set_page_config(page_title="Multi Agent App")
st.title("Multi Agent Application")

#  Sidebar CSV 
st.sidebar.header("CSV Agent")
uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])

df = None
if uploaded:
    df = pd.read_csv(uploaded)
    st.sidebar.success("CSV Loaded")
    st.sidebar.dataframe(
        pd.DataFrame({"Column": df.columns, "Type": df.dtypes.astype(str)})
    )

# CSV Tool 
@tool
def csv_sql_agent(sql_query: str):
    if df is None:
        return "No CSV uploaded."
    try:
        result = sqldf(sql_query, {"df": df})
        return result.to_string(index=False)
    except:
        return "ERROR. Write a simpler SQL query."

#Selenium Tool 
@tool
def get_sunbeam_internship_info():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    info = []

    try:
        driver.get("https://sunbeaminfo.in/internship")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

        for r in rows:
            c = r.find_elements(By.TAG_NAME, "td")
            if len(c) >= 7:
                info.append(
                    f"Batch {c[1].text} | Starts: {c[3].text} | Ends: {c[4].text} | Fees: {c[6].text}"
                )
    except:
        driver.quit()
        return "Error fetching internship data."

    driver.quit()
    return "\n".join(info)

# LLM
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

agent = create_agent(
    model=llm,
    tools=[csv_sql_agent, get_sunbeam_internship_info],
    system_prompt=(
        "You are a helpful assistant. "
        "If the user asks about CSV data, convert question into SQL for table df. "
        "If user asks about Sunbeam internships, use scraping tool. "
        "Explain answers simply."
    ),
)

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user = st.chat_input("Ask something...")

if user:
    st.session_state.messages.append({"role": "user", "content": user})

    with st.chat_message("user"):
        st.markdown(user)

    result = agent.invoke({"messages": st.session_state.messages})
    reply = result["messages"][-1].content

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
