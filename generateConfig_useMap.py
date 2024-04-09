import pandas as pd
import traceback


def generate_script(template, outfile):
    df = pd.read_excel(template, dtype='object')
    df.fillna('', inplace=True)
    cols = len(df.columns)
    for index, row in df.iterrows():
        try:
            outstr = '"' + str(row[0]).strip() + '","{'
            field = str(row[1]).strip()
            fixedString = '"":{""action"":[""useMap"",""copyData""], ""useMap"": {""values"":[{'
            sVal = '""sourceValue"":""' + str(row[2]).strip().replace('\\','\\\\').replace('"', '\\\\\\"') + '""'
            tField = '""targetField"":""' + str(row[3]).strip() + '""'
            tVal = '""targetValue"":""' + str(row[4]).strip().replace('\\','\\\\').replace('"', '\\\\\\"') + '""'
            outstr += '""' + field + fixedString + sVal + ', ' + tField + ', ' + tVal + '}]}}}"'
            outfile.write(outstr)
            outfile.write('\n')
        except Exception as err:
            print(outstr)
            print(traceback.extract_tb(err.__traceback__))
            continue