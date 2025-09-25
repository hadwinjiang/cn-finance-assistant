# https://akshare.akfamily.xyz/data/stock/stock.html#id129

import akshare as ak

news_data = ak.stock_news_em(symbol="603993")
# news_data = ak.stock_news_em(symbol="洛阳钼业")

print(news_data)

for i in range(10):
    print("\n ******")
    print(news_data.iloc[i])
    print(news_data["新闻标题"].iloc[i])
    print(news_data["发布时间"].iloc[i])
    print(news_data["新闻内容"].iloc[i])
    print(news_data["新闻链接"].iloc[i])

# uv run python AKShare/demo_stock_news.py 
