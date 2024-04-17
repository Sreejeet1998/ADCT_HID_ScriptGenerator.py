import re
import pandas as pd
import traceback

def generate_script(template, outfile):
    dfk = pd.read_excel(template, dtype='object')
    dfk['mul_sep'] = dfk['mul_sep'].fillna('')
    df = dfk.groupby(['Handle_ID', 'targetField','mul_sep']).agg({
        #'mul_sep': 'first',
        'targetValue': lambda x: x.tolist(),
        'mode': 'first'
    }).reset_index()
    print("####")
    print(df.to_string())

    df.fillna('', inplace=True)
    cols = len(df.columns)

    for index, row in df.iterrows():
        try:
            outstr = '"' + str(row[0]).strip() + '","{'
            field = str(row[1]).strip()
            mul_sep = str(row[2]).strip()
            if not mul_sep or len(mul_sep) == 0:
                data = row[3]
                setvalue = ""
                for eachval in data:
                    eachval = eachval.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
                    setvalue = setvalue + '""' + eachval + '"",'
                data = re.sub(r',$', "", string=setvalue)
            else:
                data = row[3]
                setvalue = ""
                target_value_list = []
                for eachval in data:
                    new_data = str(eachval).split(mul_sep)

                    for eachval in new_data:
                        eachval = eachval.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
                        if eachval not in target_value_list:
                            target_value_list.append(eachval)
                            setvalue = setvalue + '""' + eachval + '"",'
                data = re.sub(r',$', "", string=setvalue)

                print()
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
