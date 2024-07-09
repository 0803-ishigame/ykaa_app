import streamlit as st
import pandas as pd
import numpy as np        
from SubMain.Database import same_def

def data_list(data_path):
    data_width = 1500
    com_list = ["指定なし"]
    df_list = pd.read_excel(data_path)
    df_list = df_list.fillna("-")
    com_l = df_list["メーカー"].unique()
    for i in range(len(com_l)):
        com_list.append(com_l[i])
    col_1, col_2, col_3 = st.columns(3)
    c_select = col_1.selectbox("メーカー", com_list)
    df_list.index = df_list.index + 1
    if c_select == "指定なし":
        st.dataframe(df_list, width=data_width)
        select_df = df_list
    else:
        select_df = df_list[(df_list["メーカー"] == c_select)]
        select_df.index = np.arange(1, len(select_df)+1)
        st.dataframe(select_df, width=data_width)
def create_data(data_path):  
    st.title("新規作成")
    col1, col2 = st.columns(2)
    company2 = col1.text_input("新規メーカー名")
    dictionary = col1.checkbox("カタログ")
    if dictionary: 
        dictionary_year = col2.number_input("発行年数", 2020)
        dictionary_year = str(dictionary_year) + "年"
        dictionary2 = "◯"
    else: dictionary2 = "☓"
    etc = st.text_input("備考")
    if st.button("新規作成"):
        df_new2 = pd.DataFrame({"メーカー":[company2], "カタログ":[dictionary2], "発行年数":[str(dictionary_year)], "備考":[etc]})
        same_def.connect(data_path, df_new2)
        st.success("メーカー登録完了")