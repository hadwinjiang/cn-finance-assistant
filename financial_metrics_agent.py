#!/usr/bin/env python3
"""
Financial Metrics Analysis Tool

A command-line tool that uses the Strands Agent SDK to analyze financial metrics of stocks.
"""

import datetime as dt
from typing import Dict, Union

# Third-party imports
import yfinance as yf
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import think, http_request


@tool
def get_financial_metrics(ticker: str) -> Union[Dict, str]:
    """Fetches key financial metrics for a given stock ticker."""
    try:
        if not ticker.strip():
            return {"status": "error", "message": "Ticker symbol is required"}

        stock = yf.Ticker(ticker)
        info = stock.info

        # Get financial data
        try:
            metrics = {
                "status": "success",
                "data": {
                    "symbol": ticker,
                    "market_cap": info.get("marketCap", "N/A"),
                    "pe_ratio": info.get("trailingPE", "N/A"),
                    "forward_pe": info.get("forwardPE", "N/A"),
                    "peg_ratio": info.get("pegRatio", "N/A"),
                    "price_to_book": info.get("priceToBook", "N/A"),
                    "dividend_yield": info.get("dividendYield", "N/A"),
                    "profit_margins": info.get("profitMargins", "N/A"),
                    "revenue_growth": info.get("revenueGrowth", "N/A"),
                    "debt_to_equity": info.get("debtToEquity", "N/A"),
                    "return_on_equity": info.get("returnOnEquity", "N/A"),
                    "current_ratio": info.get("currentRatio", "N/A"),
                    "beta": info.get("beta", "N/A"),
                    "date": dt.datetime.now().strftime("%Y-%m-%d"),
                },
            }

            # Convert values to percentages where appropriate
            for key in [
                "dividend_yield",
                "profit_margins",
                "revenue_growth",
                "return_on_equity",
            ]:
                if (
                    isinstance(metrics["data"][key], (int, float))
                    and metrics["data"][key] != "N/A"
                ):
                    metrics["data"][key] = round(metrics["data"][key] * 100, 2)

            return metrics

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing financial data: {str(e)}",
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching financial metrics: {str(e)}",
        }


def create_initial_messages():
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [
                {"text": "你好，我需要帮助分析公司的财务指标"}
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "我已准备好帮助您分析财务指标。请提供公司股票代码。"
                }
            ],
        },
    ]


def create_financial_metrics_agent():
    """Create and configure the financial metrics analysis agent."""
    return Agent(
        system_prompt="""你是一名财务分析专家。请按照以下步骤执行:

<input>
当用户提供公司股票代码时：  
1. 使用 get_financial_metrics 获取数据  
2. 分析关键财务指标  
3. 按以下格式提供综合分析  
</input>

<output_format>
1. 公司概览：  
   - 市值  
   - Beta 系数  
   - 关键比率  

2. 估值指标：  
   - 市盈率 (P/E Ratio)  
   - 市盈增长比率 (PEG Ratio)  
   - 市净率 (Price to Book)  

3. 财务健康状况：  
   - 利润率  
   - 债务指标  
   - 成长性指标  

4. 投资指标：  
   - 股息信息  
   - 股本回报率 (ROE)  
   - 风险评估  
</output_format>""",
        model=BedrockModel(model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", region="us-west-2"),
        tools=[get_financial_metrics, http_request, think],
    )


def main():
    """Main function to run the financial metrics analysis tool."""
    # Create and initialize the agent
    financial_metrics_agent = create_financial_metrics_agent()
    financial_metrics_agent.messages = create_initial_messages()

    print("\n📊 Financial Metrics Analyzer 📊\n")

    while True:
        query = input("\nEnter ticker symbol> ").strip()

        if query.lower() == "exit":
            print("\nGoodbye! 👋")
            break

        print("\nAnalyzing...\n")

        try:
            # Create the user message with proper Nova format
            user_message = {
                "role": "user",
                "content": [
                    {"text": f"请分析一下这家公司的财务指标: {query}"}
                ],
            }

            # Add message to conversation
            financial_metrics_agent.messages.append(user_message)

            # Get response
            response = financial_metrics_agent(user_message["content"][0]["text"])
            print(f"Analysis Results:\n{response}\n")

        except Exception as e:
            print(f"Error: {str(e)}\n")
        finally:
            # Reset conversation after each query
            financial_metrics_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()
