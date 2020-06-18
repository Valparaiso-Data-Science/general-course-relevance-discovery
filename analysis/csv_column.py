"""##CSV Combine Function
IN:
- new_csv: name of new csv file
- old_csvs: list of old csvs
No OUT, creates one csv file of merged data from old_csvs
"""

def combine_csv(new_csv,old_csvs):
  all_files = old_csvs
  df_merged = pd.concat(all_files, ignore_index=True)
  df_merged.to_csv(new_csv,index=False)