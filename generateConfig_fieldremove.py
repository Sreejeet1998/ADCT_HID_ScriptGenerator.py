import re
import pandas as pd


def generate_script(template, outfile):
    df = pd.read_excel(template)
    df.fillna('', inplace=True)

    cols = len(df.columns)

    for index, row in df.iterrows():
        outstr = '"' + str(row[0]) + '","{'
        fieldList = str(row[1]).split(';')
        for field in fieldList:
            outstr += '""' + field.strip() +'"":{""action"":[""deleteField""]},'
        outstr = re.sub(r',$', "", string=outstr)
        outstr += '}"'
        outfile.write(outstr)
        outfile.write('\n')

