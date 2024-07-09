import pandas as pd
from io import BytesIO


def create_database_group():
    output_group = []
    df_company = pd.read_excel("./Data/メーカーDB.xlsx")
    df_goods = pd.read_excel("./Data/建材DB.xlsx")
    df_main = pd.read_excel("./Data/仕上げDB.xlsx")
    df_group = [df_main, df_company, df_goods]
    for i in df_group:
        output = BytesIO()
        i.to_excel(output, index=False)
        processed_data = output.getvalue()
        output_group.append(processed_data)
    

    return output_group

