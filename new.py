import pandas as pd
from io import StringIO

dfk = pd.read_excel(r"C:\Users\patra\OneDrive\Desktop\Arunavo B\HID_Add_Upgrade_Sample.xlsx")

dfk['mul_sep'] = dfk['mul_sep'].fillna('')
df = dfk.groupby(['Handle_ID', 'targetField', 'mul_sep']).agg({
    #'mul_sep': 'first',
    'targetValue': lambda x: x.tolist(),
    'mode': 'first'
}).reset_index()
print(df)
transformed_data = []
for index, row in df.iterrows():
    hi = str(row[0]).strip()
    tf = str(row[1]).strip()
    mul_sep = str(row[2]).strip()
    tvl = row[3]
    tvl1 = []
    if not mul_sep or len(mul_sep) == 0:
        tvl1 = tvl
        #print(tvl)
    else:
        for eachvalue in tvl:
            #print(tvl)
            new_data = str(eachvalue).split(mul_sep)
            #print('###',new_data)
            for eachvalue in new_data:
                if eachvalue not in tvl1:
                    tvl1.append(eachvalue)
                    #print("tvl=",tvl1)

    transformed_data.append({
        'Handle_ID': hi,
        'targetField': tf,
        'targetValue': tvl1,
        'mode': row['mode']
    })

    transformed_df = pd.DataFrame(transformed_data)

    # df1[''] = df1.'targetValue'.unique()
    df1 = transformed_df.groupby(['Handle_ID', 'targetField'])['targetValue'].apply(
        lambda x: list(set(y for sublist in x for y in sublist))).reset_index()

print(df1)