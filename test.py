import pandas as pd

file_path = 'combined_data.csv'
df = pd.read_csv(file_path)

# Select the specified columns and convert them to a dictionary
print(df.columns)
columns_to_dict = ['district', 'ps_name', 'spot_accident']
result_dict = df[columns_to_dict].to_dict(orient='list')