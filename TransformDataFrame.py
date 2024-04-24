import pandas as pd
from io import StringIO

def transformedDataframe(template, outfile):
    dataframe = pd.read_excel(template, dtype='object')

    dataframe['mul_sep'] = dataframe['mul_sep'].fillna('')

    dataframe = dataframe.groupby(['Handle_ID', 'targetField','mul_sep'],sort=False).agg({
        'targetValue': lambda x: x.tolist(),
        'mode': 'first'
    }).reset_index()

    transformed_data = []
    for index, row in dataframe.iterrows():
        handle_id = str(row[0]).strip()
        target_field = str(row[1]).strip()
        mul_sep = str(row[2]).strip()

        target_value = row[3]
        target_value_list = []
        if not mul_sep or len(mul_sep) == 0:
            target_value_list = target_value
        else:
            for eachvalue in target_value:
                new_data = str(eachvalue).split(mul_sep)
                for eachvalue in new_data:
                    if eachvalue not in target_value_list:
                        target_value_list.append(eachvalue)

        transformed_data.append({
            'Handle_ID': handle_id,
            'targetField': target_field,
            'targetValue': target_value_list,
            'mode': row['mode']
        })

    transformed_df = pd.DataFrame(transformed_data)
    transformed_df.fillna({"mode":"add"}, inplace=True)

    transformed_df = transformed_df.groupby(['Handle_ID', 'targetField'],sort=False).agg({
        'targetValue': lambda x: list(set(y for sublist in x for y in sublist)),
        'mode': 'first'
    }).reset_index()

    last_column = transformed_df.pop('mode')
    transformed_df.insert(3,"mode", last_column)

    return transformed_df