import re
import pandas as pd
import traceback
from TransformDataFrame import transformedDataframe

def generate_script(template, outfile):
    dataFile = transformedDataframe(template,outfile)

    for index, row in dataFile.iterrows():
        try:
            outstr = '"' + str(row[0]).strip() + '","{'
            field = str(row[1]).strip()
            setvalue = ""
            for eachval in row[2]:
                    eachval = eachval.strip().replace('\\', '\\\\\\\\').replace('"', '\\\\\\"')
                    setvalue = setvalue + '""' + eachval + '"",'
            data = re.sub(r',$', "", string=setvalue)

            mode = str(row[3]).strip()

            if mode.casefold() == "onBlank".casefold():
                mode = "onBlank"
            elif mode.casefold() == "coalesce".casefold():
                mode = "coalesce"
            else:
                mode = "add"
            outstr += '""' + field  + '"":{""action"":[""add""], ""add"":{""targetValue"":[' + data + '], ""mode"":""' + mode + '""}}}"'
            outfile.write(outstr)
            outfile.write('\n')
        except Exception as err:
            print(outstr)
            print(err)
            print(traceback.extract_tb(err.__traceback__))
            continue