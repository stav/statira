import pandas as pd
from datetime import datetime

# Read the CSV file
df = pd.read_csv('output/clients-full.csv')

# Function to convert dates to MM/DD/YYYY format
def convert_date(date_str):
    try:
        # Try parsing ISO format first
        if 'T' in str(date_str):
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        else:
            # Try parsing MM/DD/YYYY format
            date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        return date_obj.strftime('%m/%d/%Y')
    except:
        return date_str  # Return original if conversion fails

# Apply the conversion to the DOB column
df['DOB'] = df['DOB'].apply(convert_date)

# Save the result to a new file
df.to_csv('output/clients-formatted.csv', index=False) 
