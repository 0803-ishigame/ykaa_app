import streamlit as st
import pandas as pd
import numpy as np        
from SubMain.Database import same_def

def data_list(data_path):
    data_width = 1500
    com_list = ["指定なし"]
    goods_list = ["指定なし"]
    df_list = pd.read_excel(data_path)
    df_list = df_list.fillna("ー")
    com_l = df_list["メーカー"].unique()
    for i in range(len(com_l)):
        com_list.append(com_l[i])
    col_1, col_2, col_3 = st.columns(3)
    c_select = col_1.selectbox("メーカー", com_list)
    df_list_select = df_list[df_list["メーカー"] == c_select]
    goods_l = df_list_select["商品名"].unique()
    for i in range(len(goods_l)):
        goods_list.append(goods_l[i])
    g_select = col_2.selectbox("商品名", goods_list)
    df_list.index = df_list.index + 1
    if c_select == "指定なし" and g_select == "指定なし":
        st.dataframe(df_list, width=data_width)
        select_df = df_list
    elif c_select == "指定なし":
        select_df = df_list[df_list["商品名"] == g_select]
        select_df.index = np.arange(1, len(select_df)+1)
        st.dataframe(select_df, width=data_width)
    elif g_select == "指定なし":
        select_df = df_list[df_list["メーカー"] == c_select]
        select_df.index = np.arange(1, len(select_df)+1)
        st.dataframe(select_df, width=data_width)
    else:
        select_df = df_list[(df_list["メーカー"] == c_select) & (df_list["商品名"] == g_select)]
        select_df.index = np.arange(1, len(select_df)+1)
        st.dataframe(select_df, width=data_width)
def create_data(data_path, data_path2):
    com_list = ["新規メーカー"]
    g_n_list = ["新規商品名"]
    df = pd.read_excel(data_path)    
    df_com = pd.read_excel(data_path2)
    com_l = df_com["メーカー"].unique()
    for i in range(len(com_l)):
        com_list.append(com_l[i])
    st.title("新規作成")
    col1, col2, col3 = st.columns(3)
    company = col1.selectbox("メーカー", com_list)
    if company == "新規メーカー":
        col2.warning("メーカー一覧より新規作成してください")
    else:
        col_1, col_2, col_3 = st.columns(3)
        g_n_l = df[df["メーカー"] == company]["商品名"].unique()
        for i in range(len(g_n_l)):
            g_n_list.append(g_n_l[i])
        goods_name = col_1.selectbox("商品名", g_n_list)
        if goods_name == "新規商品名": 
            goods_new_name = col_1.text_input("新規商品名")
            goods_name = goods_new_name
        goods_namber = col_2.text_input("型番")
        goods_color = col_3.text_input("色番号")
        col__1, col__2 = st.columns(2)
        sample = col__1.checkbox("サンプル")
        if sample:
            sample_state = '◯'
        else: sample_state = '☓'
        
        etc = st.text_input("備考")
        if st.button("新規作成"):
            df_new = pd.DataFrame({"メーカー":[company], "商品名":[goods_name], "型番":[goods_namber], "色番号":[goods_color], "サンプル":[sample_state] ,"備考":[etc]})
            df_new = df_new.fillna("ー")
            same_def.connect(data_path, df_new)
            st.success("成功しました")
def add_data(data_path):
    df = pd.read_excel(data_path)
    company_list = []
    goods_name_list = []
    goods_number_list = []
    goods_color_list = []
    df.index = df.index + 1
    df = df.fillna("ー")
    c_ar = df['メーカー'].unique()
    for i in range(len(c_ar)):
        company_list.append(c_ar[i])
    st.title("編集")
    col1, col2, col3, col4 = st.columns(4)
    c_select = col1.selectbox('メーカー', company_list)
    g_n_ar = df[df["メーカー"] == c_select]["商品名"].unique()
    for i in range(len(g_n_ar)):
        goods_name_list.append(g_n_ar[i])
    g_n_select = col2.selectbox('商品名', goods_name_list)
    g_num_ar = df[df['商品名'] == g_n_select]["型番"].unique()
    for i in range(len(g_num_ar)):
        goods_number_list.append(g_num_ar[i])
    g_num_select = col3.selectbox('型番', goods_number_list)
    df_select = df[(df['メーカー'] == c_select) & (df['商品名'] == g_n_select) & (df['型番'] == g_num_select)]
    df = df[(df['メーカー'] != c_select) | (df['商品名'] != g_n_select) | (df['型番'] != g_num_select)]
    if df_select.empty == True:st.error("データがありません")
        #after
    else:
        goods_color = st.text_input("色番号", value=df_select.iat[0, 3])
        if df_select.iat[0, 4] == "◯":
            sample_result = True
        else: sample_result = False
        sample = st.checkbox("サンプル", value=sample_result)
        if sample: sample_after = "◯"
        else: sample_after = "☓"
        etc = st.text_input("備考", value=df_select.iat[0, 5])
        df_new = pd.DataFrame({"メーカー":[c_select], "商品名":[g_n_select], "型番":[g_num_select], "色番号":[goods_color], "サンプル":[sample_after], "備考":[etc]})
        df_new.index = df_new.index + 1
        if (df_new.iat[0,3] == df_select.iat[0,3])&(df_new.iat[0,4] == df_select.iat[0,4])&(df_new.iat[0,5] == df_select.iat[0,5]):    
            st.success("編集中")
        else:
            df = pd.concat([df, df_new])
            df.to_excel(data_path,index=False)
            st.success("保存完了")
            df_new = df_select