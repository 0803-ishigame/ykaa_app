import streamlit as st
import pandas as pd
import numpy as np
from SubMain.Database import page3_def

def page_3():
    ss = st.session_state
    data_path = "./Data/建材DB.xlsx"
    data_path2 = "./Data/メーカーDB.xlsx"
    menu_sub = ["一覧", "新規作成", "編集"]
    ss["sub_state"] = st.sidebar.selectbox("menu", menu_sub)
    if ss["sub_state"] == "一覧":
        page3_def.data_list(data_path)
    if ss["sub_state"] == "新規作成":
        page3_def.create_data(data_path, data_path2)
    if ss["sub_state"] == "編集":
        page3_def.add_data(data_path)