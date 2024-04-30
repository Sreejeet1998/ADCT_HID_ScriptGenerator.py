import pandas as pd


def generate_script(template, outfile):
    dataframe = pd.read_excel(template, dtype='object')
    flag = 0
    dataframe_header = []
    for col in dataframe.columns:
        dataframe_header.append(col)

    namingConvention = ['Handle_ID', 'sourceField', 'targetField']

    for i in range(len(dataframe_header)):
        if dataframe_header[i] == namingConvention[i]:
            pass
        else:
            flag = 1

    if flag == 0:
        dataframe.fillna('', inplace=True)
        for index, row in dataframe.iterrows():
            outstr = '"' + str(row[0]) + '","{'
            outstr += '""' + row[1] + '"":{""action"":[""copyData""],""copyData"":{""targetField"":""' + row[2] + '""}}'
            outstr += '}"'
            outfile.write(outstr)
            outfile.write('\n')
        print("Done...")
    else:
        print(template,"- Column not in right name.")