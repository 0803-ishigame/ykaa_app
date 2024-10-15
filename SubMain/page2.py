import streamlit as st
from SubMain.Database import page2_def
from SubMain import page3
from SubMain.Database import same_def

def page_2(name_ja):
    #data
    data_path = "./Data/仕上げDB.xlsx"
    data_path2 = "./Data/建材DB.xlsx"
    data_path3 = "./Data/メーカーDB.xlsx"

    #menu
    ss = st.session_state
    menu_sub = ["一覧", "新規作成", "編集", "削除"]
    ss["sub_state"] = st.sidebar.selectbox("menu", menu_sub)

    #page
    if ss["sub_state"] == "一覧":        
        page2_def.data_list(name_ja, data_path)
    if ss["sub_state"] == "新規作成":
        df_new = page2_def.new_data(data_path, data_path3)
        if st.button("新規作成"):
            same_def.connect(data_path, df_new)
            st.success("成功しました")
    if ss["sub_state"] == "編集":
        page2_def.add_data(data_path)
    if ss["sub_state"] == "削除":
        page2_def.delete_data(data_path)
