from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Set the folder directory and file name
folder_path = os.getenv("EXCEL_FOLDER_PATH")
file_name = "input_data.xlsx"

# 2. Combine them into a full path
full_path = folder_path+file_name
#print(full_path)

# 3. Read the Excel file
df = pd.read_excel(full_path)
print(df.head())

engine = create_engine(
    os.getenv("DB_URL")
)

try:
    with engine.connect() as conn:
        print("Connected Successfully")
except Exception as e:
    print("Connection Failed:", e)


'''
df.to_sql(
    "product",
    engine,
    if_exists="append",
    index=False
)
'''
