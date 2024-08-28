import pandas as pd
pd.set_option('display.width', 400)
import traceback
from TransformDataFrame import transformedDataframe

import pandas as pd
import re
import traceback
import tkinter.messagebox as messagebox


def generate_script(template, outfile):
    # Read the Excel file into a DataFrame
    dataframe = pd.read_excel(template, dtype='object')

    # Extract the column headers
    dataframe_header = dataframe.columns.tolist()

    # Define the expected naming convention
    namingConvention = ['Handle_ID', 'targetField', 'mul_sep', 'targetValue', 'mode']

    # List to hold mismatched columns
    mismatched_columns = []

    # Check if the DataFrame headers match the naming convention
    for i in range(len(namingConvention)):
        if i < len(dataframe_header) and dataframe_header[i] != namingConvention[i]:
            mismatched_columns.append(dataframe_header[i])
        elif i >= len(dataframe_header):
            mismatched_columns.append(f"Missing Column: {namingConvention[i]}")

    # Proceed only if there are no mismatched columns
    if not mismatched_columns:
        dataFile = transformedDataframe(template, outfile)
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
                outstr += '""' + field + '"":{""action"":[""add""], ""add"":{""targetValue"":[' + data + '], ""mode"":""' + mode + '""}}}"'
                outfile.write(outstr)
                outfile.write('\n')
            except Exception as err:
                print(outstr)
                print(err)
                print(traceback.extract_tb(err.__traceback__))
                continue
        print("Done...")

    else:
        mismatched_columns_str = ", ".join(mismatched_columns)
        messagebox.showerror('Python Error',
                             f'Error: Naming convention did not match! Mismatched columns: {mismatched_columns_str}')
        print(template, "- Column names do not match the expected convention.")
        print("Mismatched columns:", mismatched_columns_str)

# Ensure that the function `transformedDataframe` is defined somewhere in your code
