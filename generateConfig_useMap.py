import pandas as pd
import traceback


def generate_script(template, outfile):
    dataframe = pd.read_excel(template, dtype='object')
    flag = 0
    dataframe_header = []
    for col in dataframe.columns:
        dataframe_header.append(col)

    namingConvention = ['Hid', 'sourceField', 'sourceValue', 'targetField', 'targetValue']

    for i in range(len(dataframe_header)):
        if dataframe_header[i] == namingConvention[i]:
            pass
        else:
            flag = 1

    if flag == 0:
        dataframe.fillna('', inplace=True)
        for index, row in dataframe.iterrows():
            try:
                Hid = '"' + str(row[0]).strip() + '","{'
                sourceField = str(row[1]).strip()
                fixedString = '"":{""action"":[""useMap"",""copyData""], ""useMap"": {""values"":[{'
                sourceValue = '""sourceValue"":""' + str(row[2]).strip().replace('\\','\\\\').replace('"', '\\\\\\"') + '""'
                targetField = '""targetField"":""' + str(row[3]).strip() + '""'
                targetValue = '""targetValue"":""' + str(row[4]).strip().replace('\\','\\\\').replace('"', '\\\\\\"') + '""'
                Hid += '""' + sourceField + fixedString + sourceValue + ', ' + targetField + ', ' + targetValue + '}]}}}"'
                outfile.write(Hid)
                outfile.write('\n')
            except Exception as err:
                print(Hid)
                print(traceback.extract_tb(err.__traceback__))
                continue

        print("Done...")
    else:
        print(template,"- Column not in right name.")