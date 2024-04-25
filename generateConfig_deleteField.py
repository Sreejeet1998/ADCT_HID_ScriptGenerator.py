import re
import pandas as pd


def generate_script(template, outfile):
    dataframe = pd.read_excel(template)
    flag = 0
    dataframe_header = []
    for col in dataframe.columns:
        dataframe_header.append(col)

    namingConvention = ['Handle_ID', 'sourceField']

    for i in range(len(dataframe_header)):
        if dataframe_header[i] == namingConvention[i]:
            pass
        else:
            flag = 1

    if flag == 0:
        dataframe.fillna('', inplace=True)
        for index, row in dataframe.iterrows():
            outstr = '"' + str(row[0]) + '","{'
            fieldList = str(row[1]).split(';')
            for field in fieldList:
                outstr += '""' + field.strip() +'"":{""action"":[""deleteField""]},'
            outstr = re.sub(r',$', "", string=outstr)
            outstr += '}"'
            outfile.write(outstr)
            outfile.write('\n')
        print("Done...")
    else:
        print("Wrong Naming Convention")