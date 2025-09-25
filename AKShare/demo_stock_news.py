# https://akshare.akfamily.xyz/data/stock/stock.html#id129

import akshare as ak

stock_news_em_df = ak.stock_news_em(symbol="000960")
print(stock_news_em_df)

print(stock_news_em_df.iloc[0])
print(stock_news_em_df["新闻标题"].iloc[0])
print(stock_news_em_df["发布时间"].iloc[0])
print(repr(stock_news_em_df["新闻内容"].iloc[0]))
print(stock_news_em_df["新闻链接"].iloc[0])
print(stock_news_em_df.iloc[1])
print(stock_news_em_df["新闻标题"].iloc[1])
print(stock_news_em_df["发布时间"].iloc[1])
print(repr(stock_news_em_df["新闻内容"].iloc[1]))
print(stock_news_em_df["新闻链接"].iloc[1])
print(stock_news_em_df.iloc[2])
print(stock_news_em_df["新闻标题"].iloc[2])
print(stock_news_em_df["发布时间"].iloc[2])
print(repr(stock_news_em_df["新闻内容"].iloc[2]))
print(stock_news_em_df["新闻链接"].iloc[2])

# uv run python AKShare/demo_stock_news.py 
