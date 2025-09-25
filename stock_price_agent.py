#!/usr/bin/env python3
"""
Stock Price Analysis Tool

A command-line tool that uses the Strands Agent SDK to analyze stock prices.
"""

import datetime as dt
from typing import Dict, Union

# Third-party imports
import yfinance as yf
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import think, http_request


@tool
def get_stock_prices(ticker: str) -> Union[Dict, str]:
    """Fetches current and historical stock price data for a given ticker."""
    try:
        # Verify ticker is not empty
        if not ticker.strip():
            return {"status": "error", "message": "Ticker symbol is required"}

        # Get stock data
        stock = yf.Ticker(ticker)
        data = stock.history(period="3mo")

        if data.empty:
            return {"status": "error", "message": f"No data found for ticker {ticker}"}

        # Calculate metrics
        current_price = float(data["Close"].iloc[-1])
        previous_close = float(data["Close"].iloc[-2])
        price_change = current_price - previous_close
        price_change_percent = (price_change / previous_close) * 100

        return {
            "status": "success",
            "data": {
                "symbol": ticker,
                "current_price": round(current_price, 2),
                "previous_close": round(previous_close, 2),
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "volume": int(data["Volume"].iloc[-1]),
                "high_90d": round(float(data["High"].max()), 2),
                "low_90d": round(float(data["Low"].min()), 2),
                "date": dt.datetime.now().strftime("%Y-%m-%d"),
            },
        }

    except Exception as e:
        return {"status": "error", "message": f"Error fetching price data: {str(e)}"}


def create_initial_messages():
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [{"text": "需要帮忙分析股票价格."}],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "我已准备好为您分析股票价格。请提供公司名称或股票代码。"
                }
            ],
        },
    ]


def create_stock_price_agent():
    """Create and configure the stock price analysis agent."""
    return Agent(
        system_prompt="""你是一名股票价格分析专家。请按照以下步骤执行:

<input>
当用户提供公司名称或股票代码时：
1. 使用 get_stock_prices 获取数据  
2. 分析价格走势和趋势  
3. 按以下格式提供分析  
</input>

<output_format>
1. 价格信息：  
   - 当前价格  
   - 涨跌幅  
   - 成交量  

2. 近期表现：  
   - 90 天最高/最低价  
   - 趋势分析  

3. 关键指标摘要  
</output_format>""",
        model=BedrockModel(model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", region="us-west-2"),
        tools=[get_stock_prices, http_request, think],
    )


def main():
    """Main function to run the stock price analysis tool."""
    # Create and initialize the agent
    stock_price_agent = create_stock_price_agent()
    stock_price_agent.messages = create_initial_messages()

    print("\n🔎 股票价格分析工具 🔍\n")

    while True:
        query = input("\nSearch> ")

        if query.lower() == "exit":
            print("\nGoodbye! 👋")
            break

        print("\nSearching...\n")

        try:
            # Create the user message with proper Nova format
            user_message = {
                "role": "user",
                "content": [{"text": f"请分析下这个股票价格: {query}"}],
            }

            # Add message to conversation
            stock_price_agent.messages.append(user_message)

            # Get response
            response = stock_price_agent(user_message["content"][0]["text"])
            print(f"Results: {response}\n")

        except Exception as e:
            print(f"Error: {str(e)}\n")
        finally:
            # Reset conversation after each query
            stock_price_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()
