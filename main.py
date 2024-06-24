import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from PIL import Image
import devlopment as dev

from SubMain import page2
from SubMain import page3
from SubMain import page4

def read_passward(yaml_path):
    with open(yaml_path) as file:
        config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            credentials=config['credentials'],
            cookie_name=config['cookie']['name'],
            cookie_key=config['cookie']['key'],
            cookie_expiry_days=config['cookie']['expiry_days'],
        )
    return authenticator
def create_name_ja(name):
    if name == 'Takashi Ishigame': name_ja, job = '石亀　隆', 'スタッフ'
    if name == 'Yoshiki Katayama': name_ja, job = '片山　佳紀', '設計主任'
    if name == 'Hayato Kumagai': name_ja, job = '熊谷　颯人', 'スタッフ'
    if name == 'Yoshiharu Kikuchi': name_ja, job = '菊池　佳晴', '所長'
    if name == 'Yuko Kikuchi': name_ja, job = '菊池　祐子', '取締役'
    if name == 'Masaki Okazaki': name_ja, job = '岡崎　雅樹', '設計主任'
    name_new = [name_ja, job]
    return name_new

def main():
    #data取得
    icon = Image.open("./img/company_icon.png")
    home_img = Image.open("./img/home.jpg")
    yaml_path = "config.yaml"
    menu = ["HOME","使用仕上げ一覧", "仕様建材一覧", "メーカー一覧"]
    #pageレイアウト
    st.set_page_config(
        page_title="YKAA",
        layout="wide",
        page_icon=icon,
    )


    ## ユーザー設定読み込み
    passward = read_passward(yaml_path)

    ## UI 
    passward.login()
    if st.session_state["authentication_status"]:
        ## ログイン成功
        with st.sidebar:
            name = st.session_state["name"]
            st.image(icon)
            name_new = create_name_ja(name)
            st.markdown(f'## {name_new[0]} : {name_new[1]}')
            passward.logout('Logout', 'sidebar')
            st.divider()
            if name == "Takashi Ishigame":
                st.header("管理者")
                st.write("Download")
                DB_group = dev.create_database_group()
                st.download_button("仕上げ", DB_group[0], "仕上げDB.xlsx", use_container_width=True)
                col_1, col_2 = st.columns(2)
                col_1.download_button("メーカー", DB_group[1], "メーカーDB.xlsx", use_container_width=True)
                col_2.download_button("建材", DB_group[2], "建材DB.xlsx", use_container_width=True)
            st.session_state["app_state"] = st.selectbox("Application", menu)

        if st.session_state["app_state"] == "HOME":
            st.title("株式会社菊池佳晴建築設計事務所スタッフページ")
            st.image(home_img)

        if st.session_state["app_state"] == "使用仕上げ一覧":
            
            ##使用仕上げ一覧アプリ
            page2.page_2(name_new[0])

        if st.session_state["app_state"] == "仕様建材一覧":
            ##仕様建材一覧
            page3.page_3()

        if st.session_state["app_state"] == "メーカー一覧":
            ##メーカー一覧
            page4.page_4()




    elif st.session_state["authentication_status"] is False:
        ## ログイン失敗
        st.error('Username/password is incorrect')

main()


