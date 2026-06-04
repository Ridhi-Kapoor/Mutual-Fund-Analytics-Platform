import pandas as pd
import os

folder = "data/raw"

for file in os.listdir(folder):
    if file.endswith(".csv"):

        print("\n" + "=" * 60)
        print("FILE:", file)

        df = pd.read_csv(os.path.join(folder, file))

        # Shape
        print("\nShape:")
        print(df.shape)

        # Data Types
        print("\nData Types:")
        print(df.dtypes)

        # First 5 Rows
        print("\nFirst 5 Rows:")
        print(df.head())

        # Missing Values
        print("\nMissing Values:")
        print(df.isnull().sum())

        # Duplicate Rows
        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

