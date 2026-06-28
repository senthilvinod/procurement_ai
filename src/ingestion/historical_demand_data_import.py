import pandas as pd
import os
from src.database.connection import engine

# Read Excel
folder_path = os.getenv("EXCEL_FOLDER_PATH")
file_name = "vehicle_demand.csv"

full_path = folder_path+file_name
print(full_path)


# 3. Read the Excel file
df = pd.read_csv(full_path)
print(df.head())


df["demand_date"] = pd.to_datetime(df["demand_date"], format="%d-%m-%Y")


df["demand_date"] = df["demand_date"].dt.date

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

