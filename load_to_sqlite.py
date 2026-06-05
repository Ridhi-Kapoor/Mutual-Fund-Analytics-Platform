import pandas as pd
from sqlalchemy import create_engine, text
import os
import re

# Database configuration
DB_PATH = os.path.join('data', 'bluestock_mf.db')
engine = create_engine(f'sqlite:///{DB_PATH}')

# Directory containing cleaned CSV files
PROCESSED_DATA_DIR = os.path.join('data', 'processed')

def clean_table_name(filename):
    # Remove numbering prefix (e.g., '01_') and '_cleaned.csv' suffix
    name = re.sub(r'^\d+_', '', filename)
    name = name.replace('_cleaned.csv', '')
    return name

def load_data():
    files = [f for f in os.listdir(PROCESSED_DATA_DIR) if f.endswith('.csv')]
    files.sort()

    summary = []

    for file in files:
        file_path = os.path.join(PROCESSED_DATA_DIR, file)
        table_name = clean_table_name(file)

        print(f"Loading {file} into table '{table_name}'...")

        # Read CSV
        df = pd.read_csv(file_path)
        csv_row_count = len(df)

        # Load to SQLite
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        # Verify row count
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            sql_row_count = result.scalar()

        status = "SUCCESS" if csv_row_count == sql_row_count else "FAILURE"
        summary.append({
            "File": file,
            "Table": table_name,
            "CSV Rows": csv_row_count,
            "SQL Rows": sql_row_count,
            "Status": status
        })

    # Print summary
    print("\n" + "="*80)
    print(f"{'Table':<30} | {'CSV Rows':<10} | {'SQL Rows':<10} | {'Status':<10}")
    print("-" * 80)
    for row in summary:
        print(f"{row['Table']:<30} | {row['CSV Rows']:<10} | {row['SQL Rows']:<10} | {row['Status']:<10}")
    print("="*80)

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    load_data()
