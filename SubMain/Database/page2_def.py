import streamlit as st
import pandas as pd
import numpy as np
from SubMain.Database import create_excel
from SubMain.Database import same_def

def data_list(name_ja, data_path):
    data_width = 1500
    house_list = ["指定なし"]
    where_list = ["指定なし"]
    df = pd.read_excel(data_path)
    df = df.fillna("ー")
    df.index = df.index + 1
    h_ar = df['使用物件'].unique()
    w_ar = df['使用箇所'].unique()
    for i in range(len(h_ar)):
        house_list.append(h_ar[i])
    for i in range(len(w_ar)):
        where_list.append(w_ar[i])

    st.title("使用仕上げ一覧")
    col1, col2 = st.columns(2)
    h_select = col1.selectbox('使用物件', house_list)
    w_select = col2.selectbox('使用箇所', where_list)
    if h_select == "指定なし" and w_select == "指定なし":
        st.dataframe(df, width=data_width)
        select_df = df
    elif w_select == "指定なし":
        select_df = df[df["使用物件"] == h_select]
        select_df.index = np.arange(1, len(select_df)+1)
        st.dataframe(select_df, width=data_width)
    elif h_select == "指定なし":
        select_df = df[df["使用箇所"] == w_select]
        select_df.index = np.arange(1, len(select_df)+1)
        st.dataframe(select_df, width=data_width)
    else:
        select_df = df[(df["使用物件"] == h_select) & (df["使用箇所"] == w_select)]
        select_df.index = np.arange(1, len(select_df)+1)
        st.dataframe(select_df, width=data_width)
    df_xlsx = create_excel.creat_excel(select_df, h_select, name_ja)
    if h_select != "指定なし":
        h= h_select + "_"
        st.download_button("EXCEL保存", df_xlsx, file_name=f"{h}仕上げリスト.xlsx")
def add_data(data_path):
    df = pd.read_excel(data_path)
    house_list = []
    where_list = []
    where2_list = []
    df.index = df.index + 1
    df = df.fillna("ー")
    h_ar = df['使用物件'].unique()
    w_ar = df['使用箇所'].unique()
    w2_ar = df['使用部位'].unique()
    for i in range(len(h_ar)):
        house_list.append(h_ar[i])
    for i in range(len(w_ar)):
        where_list.append(w_ar[i])
    for i in range(len(w2_ar)):
        where2_list.append(w2_ar[i])
    st.header("検索")
    col1, col2, col3, col4 = st.columns(4)
    h_select = col1.selectbox('使用物件', house_list)
    w_select = col2.selectbox('使用箇所', where_list)
    w_2_select = col3.selectbox('使用部位', where2_list)
    df_select = df[(df['使用物件'] == h_select) & (df['使用箇所'] == w_select) & (df['使用部位'] == w_2_select)]
    df = df[(df['使用物件'] != h_select) | (df['使用箇所'] != w_select) | (df['使用部位'] != w_2_select)]
    if df_select.empty == True:st.error("データがありません")
        #after
    else:
        st.header("編集")
        col1, col2, col3 = st.columns(3)
        h_new = col1.text_input('使用物件', value=df_select.iat[0, 0])
        w_new = col2.text_input('使用箇所', value=df_select.iat[0, 1])
        w_2_new = col3.text_input('使用部位', value=df_select.iat[0, 2])
        company = col1.text_input("メーカー", value=df_select.iat[0, 3])
        goods_name = col2.text_input("商品名", value=df_select.iat[0, 4])
        goods_number = col3.text_input("型番", value=df_select.iat[0, 5])
        col_1, col_2 = st.columns(2)
        goods_color = col_1.text_input("色番号", value=df_select.iat[0, 6])
        etc = col_2.text_input("備考", value=df_select.iat[0, 7])
        df_new = pd.DataFrame({"使用物件": [h_new], "使用箇所":[w_new], "使用部位":[w_2_new], "メーカー":[company], "商品名":[goods_name], "型番":[goods_number], "色番号":[goods_color], "備考":[etc]})
        df_new.index = df_new.index + 1
        if (df_new.iat[0,0] == df_select.iat[0,0])&(df_new.iat[0,1] == df_select.iat[0,1])&(df_new.iat[0,2] == df_select.iat[0,2])&(df_new.iat[0,3] == df_select.iat[0,3])&(df_new.iat[0,4] == df_select.iat[0,4])&(df_new.iat[0,5] == df_select.iat[0,5])&(df_new.iat[0,6] == df_select.iat[0,6])&(df_new.iat[0,7] == df_select.iat[0,7]):    
            st.success("編集中")
        else:
            df = pd.concat([df, df_new])
            df.to_excel(data_path,index=False)
            st.success("保存完了")
            df_new = df_select
def new_data(data_path, data_path2):
    df = pd.read_excel(data_path2)
    company_list = ["新規メーカー"]
    goods_name_list = ["新規商品名"]
    goods_number_list = ["新規型番"]
    goods_color_list = ["新規色番号"]
    c_ar = df["メーカー"].unique()
    for i in range(len(c_ar)):
        company_list.append(c_ar[i])
    st.header("新規作成")
    house = st.text_input("使用物件")
    col1, col2 = st.columns(2)
    where = col1.text_input("使用箇所")
    where2 = col2.text_input("使用部位")
    col_1, col_2, col_3 = st.columns(3)
    company = col_1.selectbox("メーカー", company_list)
    if company == "新規メーカー":
        col_1.warning("メーカー一覧より新規作成してください")
    if company != "新規メーカー":
        company_df = df[df["メーカー"] == company]
        g_n_ar = company_df["商品名"].unique()
        for i in range(len(g_n_ar)):
            goods_name_list.append(g_n_ar[i])
        goods_name = col_2.selectbox("商品名", goods_name_list)
        if goods_name == "新規商品名":
            goods_name = col_2.text_input("新規商品名")
        if goods_name:
            goods_name_df = df[(df["メーカー"] == company) & (df["商品名"] == goods_name)]
            g_num_ar = goods_name_df["型番"].unique()
            for i in range(len(g_num_ar)):
                goods_number_list.append(g_num_ar[i])
        goods_number = col_3.selectbox("型番", goods_number_list)
        if goods_number == "新規型番":
            goods_name = col_3.text_input("新規型番")
        if goods_number:
            goods_number_df = df[(df["メーカー"] == company) & (df["商品名"] == goods_name) & (df["型番"] == goods_number)]
            g_c_ar = goods_number_df["色番号"].unique()
            for i in range(len(g_c_ar)):
                goods_color_list.append(g_c_ar[i])
        col__1, col__2 = st.columns(2)
        goods_color = col__1.selectbox("色番号", goods_color_list)
        if goods_color == "新規色番号":
            goods_color = col__2.text_input("新規色番号")
        etc = st.text_input("備考")
        df_new = pd.DataFrame({"使用物件": [house], "使用箇所":[where], "使用部位":[where2], "メーカー":[company], "商品名":[goods_name], "型番":[goods_number], "色番号":[goods_color], "備考":[etc]})
        same_def.connect(data_path, df_new)
def delete_data(data_path):
    data_width = 1000
    df = pd.read_excel(data_path)
    house_list = []
    where_list = []
    where2_list = []
    df.index = df.index + 1
    df = df.fillna("ー")
    h_ar = df['使用物件'].unique()
    w_ar = df['使用箇所'].unique()
    w2_ar = df['使用部位'].unique()
    for i in range(len(h_ar)):
        house_list.append(h_ar[i])
    for i in range(len(w_ar)):
        where_list.append(w_ar[i])
    for i in range(len(w2_ar)):
        where2_list.append(w2_ar[i])
    st.title("削除")
    col1, col2, col3, col4 = st.columns(4)
    h_select = col1.selectbox('使用物件', house_list)
    w_select = col2.selectbox('使用箇所', where_list)
    w_2_select = col3.selectbox('使用部位', where2_list)
    select_df = df[(df["使用物件"] == h_select) & (df["使用箇所"] == w_select) & (df["使用部位"] == w_2_select)]
    select_df.index = np.arange(1, len(select_df)+1)
    if select_df.empty == True:st.error("データがありません")
    else : st.dataframe(select_df, width=data_width)

    if st.button("削除"):
        df = df.drop(df[(df["使用物件"] == h_select) & (df["使用箇所"] == w_select) & (df["使用部位"] == w_2_select)].index, inplace=False)
        df.to_excel(data_path, index=False)