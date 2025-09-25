# https://akshare.akfamily.xyz/tutorial.html#id3
# 期货展期收益率

import akshare as ak

# get_roll_yield_bar_df = ak.get_roll_yield_bar(type_method="date", var="RB", start_day="20250818", end_day="20250919")

# 接口示例-历史行情数据-前复权
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20250818", end_date='20250919', adjust="qfq")
print(stock_zh_a_hist_df)

print(stock_zh_a_hist_df)

print(stock_zh_a_hist_df.iloc[-1])
print(stock_zh_a_hist_df.iloc[-2])
print(stock_zh_a_hist_df["收盘"].iloc[-1])
print(stock_zh_a_hist_df["收盘"].iloc[-2])