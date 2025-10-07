import pandas as pd
import akshare as ak

# generate dataframe with colums [code, name]
stock_info_a_code_name_df = ak.stock_info_a_code_name() 

# write to stock-code-name.csv
stock_info_a_code_name_df.to_csv('stock-code-name.csv', index=False)

# restore dataframe with colums [code, name]
stock_code_name = pd.read_csv("stock-code-name.csv")