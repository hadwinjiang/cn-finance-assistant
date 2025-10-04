
import akshare as ak

sina_info = ak.stock_financial_analysis_indicator(symbol="600000", start_year="2024")
print(sina_info)


sina_info["净利润增长率(%)"].values[-1]    # revenue_growth
sina_info["资产负债率(%)"].values[-1]  # debt_to_equity
sina_info["净资产收益率(%)"].values[-1]    #  return_on_equity


