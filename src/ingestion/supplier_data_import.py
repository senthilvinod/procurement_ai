import pandas as pd
from sqlalchemy import create_engine
from src.database.connection import *
df = pd.read_excel("D:\projects\procurement_ai\src\data\Supplier_data.xlsx") 
print(df.head())

df = df.drop(columns=["supplier_id"])
print(df.head())

df.to_sql(
    name="supplier",
    con=engine,
    if_exists="append",
    index=False
)
