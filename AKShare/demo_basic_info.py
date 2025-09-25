import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime as dt
import akshare as ak
from utils import common

code = "601127"
standard_code = common.format_stock_code(code)

info = ak.stock_individual_basic_info_xq(symbol=standard_code)
print(info)
print("\n***************")
print(info.values[1][1])
print("\n***************")
# Get company information
company_data = {
    "status": "success",
    "data": {
        "symbol": standard_code,
        "company_name": info.values[1][1], # org_name_cn 
        "sector": info.values[29][1], # classi_name 
        "industry": info.values[38][1]['ind_name'], # affiliate_industry 
        "description": info.values[5][1], # main_operation_business
        "website": info.values[19][1], # org_website   
        "register_asset": info.values[13][1], # reg_asset 
        "employees": info.values[14][1], # staff_num    
        "province": info.values[27][1],  # provincial_name 
        "date": dt.datetime.now().strftime("%Y-%m-%d"),
    },
}

print(company_data)