"""Sentiment Analysis Agent."""

from dedalus_labs import AsyncDedalus, DedalusRunner
from typing import Dict, Any

from ..config import config
from ..tools import score_sentiment, analyze_news_sentiment


class SentimentAgent:
    """Agent specializing in sentiment analysis."""

    def __init__(self):
        self.name = "Sentiment Analysis Agent"
        self.model = config.sentiment_model
        self.mcp_servers = [config.brave_search_mcp, config.exa_mcp]
        self.tools = [score_sentiment, analyze_news_sentiment]

    async def analyze(self, stock_ticker: str) -> Dict[str, Any]:
        """
        Perform comprehensive sentiment analysis.

        Args:
            stock_ticker: Stock ticker symbol (e.g., "TSLA", "AAPL")

        Returns:
            Dictionary containing agent name and analysis results
        """
        client = AsyncDedalus()
        runner = DedalusRunner(client)

        prompt = f"""You are a sentiment analysis expert. Conduct a thorough sentiment analysis of {stock_ticker}.

Your analysis should cover:

1. **News Sentiment**:
   - Recent news articles (past 30 days)
   - Major news events and their impact
   - Media tone and coverage frequency
   - Sentiment trends over time

2. **Analyst Sentiment**:
   - Recent analyst ratings (buy/hold/sell)
   - Rating changes and upgrades/downgrades
   - Price target changes
   - Analyst consensus and divergence

3. **Social Media & Retail Sentiment**:
   - Social media mentions and trends
   - Retail investor sentiment
   - Community discussions and debates
   - Influencer opinions

4. **Management & Insider Activity**:
   - Management reputation and track record
   - Recent insider buying or selling
   - Executive compensation alignment
   - Corporate governance quality

5. **Market Sentiment Indicators**:
   - Short interest levels and trends
   - Options market sentiment (put/call ratios)
   - Institutional ownership changes
   - Fund flows and positioning

6. **Forward-Looking Sentiment**:
   - Upcoming catalysts (earnings, product launches, etc.)
   - Market expectations vs. reality
   - Potential sentiment drivers

**Search Strategy**:
- Use Brave Search for recent news articles and analyst reports
- Use Exa for semantic search of sentiment and opinion pieces
- Look for recent insider trading activity
- Find social media trends and discussions
- Search for analyst rating changes

**Sentiment Scoring**:
- Use the score_sentiment tool on news headlines and summaries
- Aggregate sentiment across multiple sources
- Identify sentiment shifts and momentum

**Output Format**:
Provide a structured analysis with:
- Overall sentiment score and classification (bullish/bearish/neutral)
- News sentiment summary with key headlines
- Analyst consensus and recent changes
- Social/retail sentiment assessment
- Management and insider activity analysis
- Upcoming catalysts or concerns
- Your overall sentiment perspective: BULLISH, BEARISH, or NEUTRAL
- Confidence level (1-10)

Be comprehensive and cite specific sources. This analysis will be part of a debate with other agents."""

        try:
            result = await runner.run(
                input=prompt,
                model=self.model,
                tools=self.tools,
                mcp_servers=self.mcp_servers,
                stream=False
            )

            return {
                "agent": "sentiment",
                "agent_name": self.name,
                "analysis": result.final_output,
                "status": "success"
            }

        except Exception as e:
            return {
                "agent": "sentiment",
                "agent_name": self.name,
                "analysis": f"Error during analysis: {str(e)}",
                "status": "error"
            }
