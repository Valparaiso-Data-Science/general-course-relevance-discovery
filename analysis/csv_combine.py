def combine_csv(new_csv,old_csvs):
  all_files = old_csvs
  df_merged = pd.concat(all_files, ignore_index=True)
  df_merged.to_csv(new_csv,index=False)
