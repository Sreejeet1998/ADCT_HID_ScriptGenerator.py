import re
import pandas as pd
import traceback


dfk = pd.read_excel(r"C:\Users\patra\OneDrive\Desktop\Arunavo B\HID_Add_Upgrade_Sample.xlsx")

dfk['mul _sep'] = dfk['mul _sep'].fillna('')

template = dfk.groupby(['Handle_ID', 'targetField']).agg({
    'mul _sep': 'first',
    'targetValue': lambda x: ','.join(x),
    'mode': 'first'
}).reset_index()

def generate_script(template, outfile):
    # default header index is 0 i.e., the first row. Default parser include first row as header.
    # To set no header parser set header=None.
    df = pd.read_excel(template, dtype='object')
    df.fillna('', inplace=True)
    cols = len(df.columns)

    for index, row in df.iterrows():
        try:
            outstr = '"' + str(row[0]).strip() + '","{'
            field = str(row[1]).strip()
            targetFieldSep = str(row[2]).strip()
            if not targetFieldSep or len(targetFieldSep) == 0:
                data = str(row[3]).strip()
                data = data.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
                data = '""' + data + '""'
            else:
                data = str(row[3]).split(targetFieldSep)
                # print(data)
                setvalue = ""
                for eachval in data:
                    eachval = eachval.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
                    setvalue = setvalue + '""' + eachval + '"",'
                data = re.sub(r',$', "", string=setvalue)
            mode = str(row[4]).strip()
            if mode.casefold() == "onBlank".casefold():
                mode = "onBlank"
            elif mode.casefold() == "coalesce".casefold():
                mode = "coalesce"
            else:
                mode = "add"
            outstr += '""' + field + '"":{""action"":[""add""], ""add"":{""targetValue"":[' + data + '], ""mode"":""' + mode + '""}}}"'
            outfile.write(outstr)
            outfile.write('\n')
        except Exception as err:
            print(outstr)
            print(err)
            print(traceback.extract_tb(err.__traceback__))
            continue
