import pandas as pd


def generate_script(template, outfile):
    df = pd.read_excel(template, dtype='object')
    #####################################
    df.fillna('', inplace=True)
    cols = len(df.columns)
    for index, row in df.iterrows():
        outstr = '"' + str(row[0]) + '","{'
        outstr += '""' + row[1] + '"":{""action"":[""copyData""],""copyData"":{""targetField"":""' + row[2] + '""}}'
        outstr += '}"'
        outfile.write(outstr)
        outfile.write('\n')
