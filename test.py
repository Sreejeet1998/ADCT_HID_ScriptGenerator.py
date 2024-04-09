import pandas as pd

text = """Handle_ID	targetField	mul _sep	targetValue	mode
abcd/1234	dc.sample.field1		article,technicalReport	add
abcd/1234	dc.sample.field2	;	eng;hin	add
abcd/4567	dc.sample.field1	||	ug||pg	add
abcd/8910	dc.sample.field2		ug,pg	coalesce
"""

# Create dataframe
df = pd.DataFrame([x.split('\t') for x in text.splitlines()[1:]],
                  columns=[x for x in text.splitlines()[0].split('\t')])

# Fill nan values with empty string
df['mul_sep'] = df['mul_sep'].fillna('')

def target_list(x):
  # Split values considering delimiters and quotes
  return eval(x.tolist()[0].replace('"', '').replace("'", ''))

# Group and aggregate
df = df.groupby(['Handle_ID', 'targetField']).agg({
    'mul _sep': 'first',
    'targetValue': target_list,
    'mode': 'first'
}).reset_index()

# Print specific rows
print(df.iloc[0]['targetValue'])  # Print first row targetValue as list
print(df.iloc[-1]['targetValue']) # Print last row targetValue as list
print(df)