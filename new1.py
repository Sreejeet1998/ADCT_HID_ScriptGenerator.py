import pandas as pd

# Read Excel file
df = pd.read_excel(r"C:\Users\patra\OneDrive\Desktop\Arunavo B\HID_Add_Upgrade_Sample.xlsx")

# Function to create JSON-like string for each row
def create_json_string(row):
    handle_id = str(row[0]).strip()
    target_field = str(row[1]).strip()
    mul_sep = str(row[2]).strip()

    if not mul_sep or len(mul_sep) == 0:
        data = str(row[3]).strip()
        data = data.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
        data = '""' + data + '""'
    else:
        data = str(row[3]).split(mul_sep)
        # print(data)
    target_values = row['targetValue'].split(row['mul_sep'])  # Handle multiple separators
    mode = row['mode']

    json_dict = {
        "action": ["add"],
        "add": {
            "targetValue": target_values,
            "mode": mode
        }
    }

    json_string = f'{{{target_field}:{json_dict}}}'
    return f'{handle_id},{json_string}'

# Group by Handle_ID and targetField, then keep only the first row (assuming distinct target fields)
grouped_df = df.groupby(['Handle_ID', 'targetField']).head(1)

# Apply the function to each row and create a new DataFrame
csv_data = grouped_df.apply(create_json_string, axis=1)

# Save as CSV
csv_data.to_csv('output.csv', index=False, header=False)
