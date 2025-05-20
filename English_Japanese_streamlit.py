# Filename: W1208_GenAI_LC_RAG_08_streamlit.py
# ========================
# LangChain RAG + Streamlit GUI 介面
# ========================

#!pip install pypdf chromadb streamlit

import os
import datetime
from dotenv import load_dotenv
import openai
import streamlit as st

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import (RecursiveCharacterTextSplitter)
from langchain_chroma import Chroma
from langchain.schema import HumanMessage
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_key)

st.title("日英雙語學習小工具")

lang = st.radio("選擇語言", ["English", "日本語"])

word = st.text_input(f"請輸入要查的{lang}單字")

if "word_list" not in st.session_state:
    st.session_state.word_list = []

if st.button("查詢單字"):
    if word.strip():
        prompt = f"請用{lang}解釋以下單字，並造一個例句:\n單字: {word}"
        response = llm.invoke([HumanMessage(content=prompt)])
        st.markdown(f"**解釋與例句:**\n{response.content}")
        if word not in st.session_state.word_list:
            st.session_state.word_list.append(word)

if st.session_state.word_list:
    st.markdown("### 背誦清單")
    for w in st.session_state.word_list:
        st.write(w)
