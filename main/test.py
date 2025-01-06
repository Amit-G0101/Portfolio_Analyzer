import pandas as pd
from datetime import datetime
import re

# List of file names
file_names = ['MW-NIFTY-TOTAL-MARKET-05-Jan-2025.csv', 'MW-NIFTY-TOTAL-MARKET-30-Dec-2024.csv']

# Create a DataFrame with file names
df = pd.DataFrame(file_names, columns=["file_name"])

date_pattern=r"(\d{2})-(\w{3})-(\d{4})"
# Extract the date from the file name and convert it to datetime
df['date'] = df['file_name'].apply(lambda x: datetime.strptime(re.search(date_pattern,x).group(), '%d-%b-%Y'))

# Sort the DataFrame by the 'date' column in descending order
df_sorted = df.sort_values(by="date", ascending=False)

# Select the latest file (first row after sorting)
latest_file = df_sorted.iloc[0]

# Output the latest file
print(latest_file["file_name"])
