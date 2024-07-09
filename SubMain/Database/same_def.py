import pandas as pd

def connect(data_path, df_new):
    df = pd.read_excel(data_path)
    df = pd.concat([df, df_new])
    df.to_excel(data_path, index=False)