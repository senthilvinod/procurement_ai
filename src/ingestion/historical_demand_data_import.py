import pandas as pd
import os
from src.database.connection import engine

# Read Excel
folder_path = os.getenv("EXCEL_FOLDER_PATH")
file_name = "demand_data.xlsx"

full_path = folder_path+file_name
print(full_path)

# 3. Read the Excel file
df = pd.read_excel(full_path)
print(df.head())

table_name = "vehicle_demand_history"  

try:
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",   # append records
        index=False
    )

    print(f"Imported into {table_name}")

except Exception as e:
    print(f"Failed importing {table_name}")
    print(e)

print("\nData import completed")
