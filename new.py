import re
import pandas as pd
import traceback
import time

dfk = pd.read_excel(r"C:\Users\patra\OneDrive\Desktop\Arunavo B\HID_Add_Upgrade_Sample.xlsx")

dfk['mul _sep'] = dfk['mul _sep'].fillna('')

df = dfk.groupby(['Handle_ID', 'targetField']).agg({
    'mul _sep': 'first',
    'targetValue': lambda x: ','.join(x),
    'mode': 'first'
}).reset_index()


print(df)
# df = pd.read_excel(template, dtype='object')
# df.fillna('', inplace=True)
# cols = len(df.columns)

for index, row in df.iterrows():
    #try:
        # print(row[0],row[1],row[2],row[3],row[4])
        outstr = '"' + str(row[0]).strip() + '","{'
        field = str(row[1]).strip()
        mul_sep = str(row[2]).strip()


        if not mul_sep or len(mul_sep) == 0:
            data = str(row[3]).strip()
            data = data.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
            print(data)
            data = '""' + data + '""'

        else:
            data = str(row[3]).split(mul_sep)
            # print(data)
            setvalue = ""
            for eachval in data:
                eachval = eachval.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
                setvalue = setvalue + '""' + eachval + '"",'
            data = re.sub(r',$', "", string=setvalue)
        mode = str(row[4]).strip()
        mode = str(row[4])
        if mode.casefold() == "onBlank".casefold():
            mode = "onBlank"
        elif mode.casefold() == "coalesce".casefold():
            mode = "coalesce"
        else:
            mode = "add"

        outstr += '""' + field + '"":{""action"":[""add""], ""add"":{""targetValue"":[' + data + '], ""mode"":""' + mode + '""}}}"'
        # outfile.write(outstr)
        # outstrip.write('\n')
        print(outstr)

    # except Exception as err:
    #     print(outstr)
    #     print(err)
    #     print(traceback.extract_tb(err.__traceback__))
    #     continue
