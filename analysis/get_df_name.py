"""##Retrieve Dataframe Name Function
IN:
- df: dataframe
OUT:
- name: name of dataframe
"""

def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name
