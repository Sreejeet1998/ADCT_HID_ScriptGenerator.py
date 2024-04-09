import re
import pandas as pd
import traceback

dfk = pd.read_excel(r"C:\Users\patra\OneDrive\Desktop\Arunavo B\HID_Add_Upgrade_Sample.xlsx")

dfk['mul _sep'] = dfk['mul _sep'].fillna('')
df = dfk.groupby(['Handle_ID', 'targetField']).agg({
    
    'mul _sep': 'first',
    'targetValue': lambda x: x.tolist(),
    'mode': 'first'
}).reset_index()

#print(df)
# def generate_script(template, outfile):
#df = pd.read_excel(template, dtype='object')
df.fillna('', inplace=True)
cols = len(df.columns)

for index, row in df.iterrows():
    try:
        # print(row[0],row[1],row[2],row[3],row[4])
        outstr = '"' + str(row[0]).strip() + '","{'
        field = str(row[1]).strip()
        mul_sep = str(row[2]).strip()

        if not mul_sep or len(mul_sep) == 0:
            data = row[3]
            #print("---",data)
            #print(type(data))
            setvalue = ""
            for eachval in data:
                eachval = eachval.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
                #print("####",eachval)
                setvalue = setvalue + '""' + eachval + '"",'
                #print(setvalue)
            data = re.sub(r',$', "", string=setvalue)
            #print(data)
        else:
            #data = str(row[3]).split(mul_sep)
            data = row[3]
            # print(type(data))
            setvalue = ""
            for eachval in data:
                #print(eachval)
                adata = str(eachval).split(mul_sep)
                for eachval in adata:
                    #print(eachval)
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
        # outfile.write(outstr)
        # outstrip.write('\n')
        print(outstr)

    except Exception as err:
        #print(outstr)
        print(err)
        print(traceback.extract_tb(err.__traceback__))
        continue
