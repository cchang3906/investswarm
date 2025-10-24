"""Financial Analysis Agent."""

from dedalus_labs import AsyncDedalus, DedalusRunner
from typing import Dict, Any

from ..config import config
from ..tools import (
    calculate_financial_ratios,
    calculate_valuation_metrics,
    analyze_growth_trends,
    execute_python_code,
)


class FinancialAgent:
    """Agent specializing in financial analysis of stocks."""

    def __init__(self):
        self.name = "Financial Analysis Agent"
        self.model = config.financial_model
        self.mcp_servers = [config.brave_search_mcp]
        self.tools = [
            calculate_financial_ratios,
            calculate_valuation_metrics,
            analyze_growth_trends,
            execute_python_code,
        ]

    async def analyze(self, stock_ticker: str) -> Dict[str, Any]:
        """
        Perform comprehensive financial analysis of a stock.

        Args:
            stock_ticker: Stock ticker symbol (e.g., "TSLA", "AAPL")

        Returns:
            Dictionary containing agent name and analysis results
        """
        client = AsyncDedalus()
        runner = DedalusRunner(client)

        prompt = f"""You are a financial analysis expert. Conduct a thorough financial analysis of {stock_ticker}.

Your analysis should cover:

1. **Financial Health**:
   - Search for the latest financial statements (balance sheet, income statement, cash flow)
   - Calculate or find key financial ratios: profit margin, ROE, ROA, debt-to-equity
   - Assess liquidity and solvency

2. **Profitability Analysis**:
   - Revenue trends over the past 3-5 years
   - Net income and earnings growth
   - Profit margins compared to industry averages
   - EBITDA and operating income trends

3. **Valuation Metrics**:
   - P/E ratio, P/S ratio, P/B ratio
   - EV/EBITDA, EV/Sales
   - Compare to sector peers and historical averages

4. **Cash Flow Analysis**:
   - Operating cash flow trends
   - Free cash flow generation
   - Capital expenditure requirements

5. **Balance Sheet Strength**:
   - Debt levels and debt maturity profile
   - Cash reserves and liquidity
   - Asset quality

**Search Strategy**:
- Use web search to find the latest quarterly and annual reports
- Look for recent earnings calls and financial news
- Find analyst reports and financial data from reputable sources

**Output Format**:
Provide a structured analysis with:
- Key financial metrics (with numbers)
- Trend analysis
- Strengths and weaknesses
- Your overall financial perspective: BULLISH, BEARISH, or NEUTRAL
- Confidence level (1-10)
- Specific concerns or red flags

Be data-driven and cite specific numbers. This analysis will be part of a debate with other agents."""

        try:
            result = await runner.run(
                input=prompt,
                model=self.model,
                tools=self.tools,
                mcp_servers=self.mcp_servers,
                stream=False
            )

            return {
                "agent": "financial",
                "agent_name": self.name,
                "analysis": result.final_output,
                "status": "success"
            }

        except Exception as e:
            return {
                "agent": "financial",
                "agent_name": self.name,
                "analysis": f"Error during analysis: {str(e)}",
                "status": "error"
            }
