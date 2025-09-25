import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, date 
from utils import common

today = date.today()
result = common.format_date(today)
print(result)

standard_code = common.format_stock_code("600001")
print(standard_code)