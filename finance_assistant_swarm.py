#!/usr/bin/env python3
"""
Finance Assistant Swarm Agent

A collaborative swarm of specialized agents for comprehensive stock analysis.
"""
# Standard library imports
import logging
import time
from typing import Dict, Any, List

# Third-party imports
from strands import Agent, tool
from strands.models import BedrockModel
from strands.multiagent import Swarm
from strands_tools import think
import yfinance as yf

from stock_price_agent import get_stock_prices, create_stock_price_agent
from financial_metrics_agent import get_financial_metrics, create_financial_metrics_agent
from company_analysis_agent import get_company_info, get_stock_news, create_company_analysis_agent

# Enable debug logs
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

@tool
def get_real_stock_data(ticker: str) -> Dict[str, Any]:
    """Get accurate stock data outside the swarm"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")
        
        if hist.empty:
            return {"status": "error", "message": f"No data found for {ticker}"}
        
        current_price = round(float(hist["Close"].iloc[-1]), 2)
        prev_close = round(float(hist["Close"].iloc[-2]), 2) if len(hist) > 1 else current_price
        price_change = round(current_price - prev_close, 2)
        price_change_pct = round((price_change / prev_close) * 100, 2) if prev_close != 0 else 0
        
        return {
            "status": "success",
            "ticker": ticker.upper(),
            "current_price": current_price,
            "price_change": price_change,
            "price_change_pct": price_change_pct,
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "volume": int(hist["Volume"].iloc[-1]),
            "revenue": info.get("totalRevenue"),
            "employees": info.get("fullTimeEmployees"),
            "sector": info.get("sector"),
            "industry": info.get("industry")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@tool
def analyze_company_with_collaborative_swarm(query: str, stock_data: str = "") -> Dict[str, Any]:
    """Collaborative swarm using Nova LITE to avoid streaming timeouts"""
    try:
        # ticker = query.upper() if len(query) <= 5 else "AMZN"
        ticker = query.upper() 
        
        # Use NOVA LITE for all swarm agents - much faster, no timeouts
        company_strategist = Agent(
            name="company_strategist",
            system_prompt=f"分析 {ticker} 的商业模式。先使用 get_company_info，然后交由 financial_analyst 处理。",
            model=BedrockModel(model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", region="us-west-2"),
            tools=[get_company_info]
        )
        
        financial_analyst = Agent(
            name="financial_analyst", 
            system_prompt=f"基于公司insights，展开分析。先使用 get_financial_metrics，然后交由 market_analyst 处理。 ",
            model=BedrockModel(model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", region="us-west-2"),
            tools=[get_financial_metrics]
        )
        
        market_analyst = Agent(
            name="market_analyst",
            system_prompt=f"综合所有见解。使用 get_stock_news 提供最终建议。",
            model=BedrockModel(model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", region="us-west-2"),
            tools=[get_stock_news]
        )
        
        swarm = Swarm(
            [company_strategist, financial_analyst, market_analyst],
            max_handoffs=3,
            max_iterations=3,
            execution_timeout=120.0,
            node_timeout=30.0
        )
        
        result = swarm(f"Analyze {ticker}")
        
        return {
            "status": "success",
            "collaborative_analysis": result.final_response,
            "collaboration_path": [node.node_id for node in result.node_history]
        }
    except Exception as e:
        return {"status": "error", "collaborative_analysis": f"Analysis failed: {str(e)}"}

def create_orchestration_agent() -> Agent:
    """Orchestrator with Nova Pro for deep synthesis"""
    return Agent(
        system_prompt="""你是一名资深金融公司研究总监。

        工作流程 (WORKFLOW):  
        1. 使用 get_real_stock_data 获取真实股票数据  
        2. 使用 analyze_company_with_collaborative_swarm 获取一次协作分析  
        3. 使用 think 工具综合分析，形成深度战略洞察  

        关键规则 (CRITICAL RULES):  
        - 禁止多次调用 analyze_company_with_collaborative_swarm  
        - 聚焦于综合与战略结论  
        - 必须突出显示当前股价  
        - 提供能够体现协作智能体价值的深度洞察  

        报告结构 (REPORT STRUCTURE):  
        1. 执行摘要（当前股价 + 核心论点）  
        2. 战略业务分析（基于智能体协作提起到的洞察）  
        3. 财务健康评估（整合指标）  
        4. 市场情绪分析（新闻 + 趋势）  
        5. 投资建议（买入/持有/卖出及其理由）""",
        model=BedrockModel(model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0", region="us-west-2"),
        tools=[get_real_stock_data, analyze_company_with_collaborative_swarm, think],
    )

def create_initial_messages() -> List[Dict]:
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [{"text": "你好，我需要帮助，分析公司的股票。"}],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "我已准备好利用实时数据和多智能体的协作分析，为您提供全面的股票分析。请提供公司名称或股票代码。"
                }
            ],
        },
    ]

def main():
    """Main function to run the finance assistant swarm."""
    # Create the orchestration agent
    orchestration_agent = create_orchestration_agent()

    # Initialize messages for the orchestration agent
    orchestration_agent.messages = create_initial_messages()

    print("\n🤖 Hybrid Multi-Agent Stock Analysis (Nova Lite Swarm + Nova Pro Synthesis) 📊")
    print("Features: Real-time data + Fast collaborative swarm + Deep orchestrator synthesis\n")

    while True:
        query = input("\nWhat company would you like to analyze? (or 'exit' to quit)> ")

        if query.lower() == "exit":
            print("\nGoodbye! 👋")
            break

        print("\nInitiating hybrid collaborative analysis...\n")

        try:
            # Create the user message with proper Nova format
            user_message = {
                "role": "user",
                "content": [
                    {
                        "text": f"请使用真实股票数据和协作多智能体分析来分析{query}。确保各智能体在彼此见解的基础上进行拓展，并提供全面的战略分析。请突出显示当前股价。 "
                    }
                ],
            }

            # Add message to conversation
            orchestration_agent.messages.append(user_message)

            # Get response
            response = orchestration_agent(user_message["content"][0]["text"])

            # Format and print response
            if isinstance(response, dict) and "content" in response:
                print("\nHybrid Collaborative Analysis Results:")
                for content in response["content"]:
                    if "text" in content:
                        print(content["text"])
            else:
                print(f"\nHybrid Collaborative Analysis Results:\n{response}\n")

        except Exception as e:
            print(f"Error: {str(e)}\n")
            if "ThrottlingException" in str(e):
                print("Rate limit reached. Waiting 10 seconds before retry...")
                time.sleep(10)
                continue
        finally:
            # Reset conversation after each query to maintain clean context
            orchestration_agent.messages = create_initial_messages()
            
if __name__ == "__main__":
    main()
