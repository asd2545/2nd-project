import pandas as pd
from datetime import datetime

def clean_data():
    input_file_name = "raw_data_scraped_on 14-07-2025.csv"
    
    try:
        df = pd.read_csv(input_file_name)
        print(f"Successfully loaded: {input_file_name}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file_name}' was not found.")
        return
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return

    df.fillna('N/A', inplace=True)
    df.drop_duplicates(inplace=True)

    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].str.strip()
            df[column] = df[column].str.title()

    current_time = datetime.now()
    timestamp_str = current_time.strftime("%d-%m-%Y")
    output_file_name = f"cleaned_data_on {timestamp_str}.csv"
    
    try:
        df.to_csv(output_file_name, index=False, encoding='utf-8-sig')
        print(f"Successfully created cleaned data file: {output_file_name}")
    except Exception as e:
        print(f"Error saving cleaned CSV file: {e}")

if __name__ == "__main__":
    clean_data()
