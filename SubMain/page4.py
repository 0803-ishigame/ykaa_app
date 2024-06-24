import streamlit as st
from SubMain.Database import page4_def

def page_4():
    ss = st.session_state
    data_path = "./Data/メーカーDB.xlsx"
    menu_sub = ["一覧", "新規作成", "編集"]
    ss["sub_state"] = st.sidebar.selectbox("menu", menu_sub)
    if ss["sub_state"] == "一覧":
        page4_def.data_list(data_path)
    if ss["sub_state"] == "新規作成":
        page4_def.create_data(data_path)