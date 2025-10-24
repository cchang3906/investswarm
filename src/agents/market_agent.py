"""Market and Product Analysis Agent."""

from dedalus_labs import AsyncDedalus, DedalusRunner
from typing import Dict, Any

from ..config import config


class MarketAgent:
    """Agent specializing in market and product analysis."""

    def __init__(self):
        self.name = "Market & Product Analysis Agent"
        self.model = config.market_model
        self.mcp_servers = [config.brave_search_mcp, config.exa_mcp]
        self.tools = []  # Market analysis primarily uses search

    async def analyze(self, stock_ticker: str) -> Dict[str, Any]:
        """
        Perform comprehensive market and product analysis.

        Args:
            stock_ticker: Stock ticker symbol (e.g., "TSLA", "AAPL")

        Returns:
            Dictionary containing agent name and analysis results
        """
        client = AsyncDedalus()
        runner = DedalusRunner(client)

        prompt = f"""You are a market and product analysis expert. Conduct a thorough market analysis of {stock_ticker}.

Your analysis should cover:

1. **Market Position & Size**:
   - Total Addressable Market (TAM) size and growth rate
   - Company's current market share
   - Market dynamics and trends
   - Geographic presence and expansion opportunities

2. **Competitive Landscape**:
   - Key competitors and their market shares
   - Competitive advantages and disadvantages
   - Barriers to entry in the market
   - Competitive threats (new entrants, substitutes)

3. **Product Analysis**:
   - Core products/services and their differentiation
   - Product portfolio strength and diversity
   - Innovation pipeline and R&D effectiveness
   - Product quality and customer satisfaction

4. **Economic Moat**:
   - Network effects
   - Brand strength and customer loyalty
   - Cost advantages
   - Switching costs
   - Regulatory advantages
   - Intellectual property and patents

5. **Growth Opportunities**:
   - New market opportunities
   - Product expansion potential
   - Strategic partnerships and acquisitions
   - Industry tailwinds and secular trends

6. **Market Risks**:
   - Competitive pressures
   - Market saturation
   - Technological disruption
   - Regulatory changes

**Search Strategy**:
- Use Exa for deep semantic search on market research and industry reports
- Use Brave Search for recent market news and competitive intelligence
- Look for industry analyst reports, market research, and competitive analyses
- Find customer reviews, product comparisons, and expert opinions

**Output Format**:
Provide a structured analysis with:
- Market size and growth metrics
- Competitive positioning assessment
- Product strength evaluation
- Moat analysis (wide/narrow/none)
- Growth potential assessment
- Your overall market perspective: BULLISH, BEARISH, or NEUTRAL
- Confidence level (1-10)
- Key opportunities and threats

Be specific and cite sources. This analysis will be part of a debate with other agents."""

        try:
            result = await runner.run(
                input=prompt,
                model=self.model,
                mcp_servers=self.mcp_servers,
                stream=False
            )

            return {
                "agent": "market",
                "agent_name": self.name,
                "analysis": result.final_output,
                "status": "success"
            }

        except Exception as e:
            return {
                "agent": "market",
                "agent_name": self.name,
                "analysis": f"Error during analysis: {str(e)}",
                "status": "error"
            }
