def rename_col(csv, og_name, new_name):
    csv.rename(columns={og_name:new_name},inplace=True)
