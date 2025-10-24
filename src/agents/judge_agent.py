"""Judge Agent - Synthesizes research and provides final verdict."""

from dedalus_labs import AsyncDedalus, DedalusRunner
from typing import List, Dict, Any

from ..config import config


class JudgeAgent:
    """Agent that judges the debate and provides final verdict."""

    def __init__(self):
        self.name = "Judge & Verdict Agent"
        self.models = config.judge_models
        self.mcp_servers = []  # Judge doesn't need external search

    async def judge(self, research_results: List[Dict[str, Any]], stock_ticker: str) -> Dict[str, Any]:
        """
        Judge the debate between agents and provide final verdict.

        Args:
            research_results: List of analysis results from all agents
            stock_ticker: Stock ticker symbol

        Returns:
            Dictionary containing final verdict
        """
        client = AsyncDedalus()
        runner = DedalusRunner(client)

        # Compile all research into context
        context_parts = []
        for result in research_results:
            if result["status"] == "success":
                context_parts.append(
                    f"{'=' * 80}\n"
                    f"{result['agent_name'].upper()}\n"
                    f"{'=' * 80}\n\n"
                    f"{result['analysis']}\n"
                )
            else:
                context_parts.append(
                    f"{'=' * 80}\n"
                    f"{result['agent_name'].upper()} - ERROR\n"
                    f"{'=' * 80}\n\n"
                    f"{result['analysis']}\n"
                )

        full_context = "\n".join(context_parts)

        prompt = f"""You are a senior investment analyst and portfolio manager with decades of experience. You are judging a debate between three AI agents who have researched {stock_ticker} from different perspectives.

RESEARCH FINDINGS:
{full_context}

YOUR TASK:

As an impartial judge, synthesize these analyses and provide a comprehensive investment verdict.

**Step 1: Analyze Each Perspective**
- Summarize the key arguments from the Financial Analysis Agent
- Summarize the key arguments from the Market & Product Analysis Agent
- Summarize the key arguments from the Sentiment Analysis Agent
- Note the perspective (bullish/bearish/neutral) and confidence level of each

**Step 2: Identify Agreements and Conflicts**
- Where do the agents agree? What consensus exists?
- Where do they disagree? What are the key points of contention?
- Are there contradictions that need to be resolved?
- Which arguments are most compelling and evidence-based?

**Step 3: Weigh the Evidence**
- Evaluate the strength of financial fundamentals
- Assess the competitive position and market opportunity
- Consider the sentiment and momentum factors
- Identify the most critical factors for this investment decision

**Step 4: Consider Risk and Opportunity**
- What are the key risks identified across analyses?
- What are the main growth opportunities?
- What could go wrong? (downside scenarios)
- What could go right? (upside scenarios)
- What is the risk/reward profile?

**Step 5: Provide Final Verdict**

Your verdict must include:

1. **Investment Recommendation**: BUY, HOLD, or SELL
   - Be clear and decisive

2. **Conviction Level**: Rate your confidence from 1-10
   - 1-3: Low conviction, high uncertainty
   - 4-6: Moderate conviction, some uncertainty
   - 7-10: High conviction, strong evidence

3. **Price Target or Timeframe** (if applicable):
   - Expected return potential
   - Investment timeframe (short/medium/long term)

4. **Key Reasoning**:
   - 3-5 bullet points explaining your decision
   - Focus on the most critical factors
   - Be specific and data-driven

5. **Main Risks**:
   - Top 3 risks to your thesis
   - What would make you change your mind?

6. **Monitoring Points**:
   - What metrics or events should investors watch?
   - What would validate or invalidate this thesis?

**IMPORTANT GUIDELINES**:
- Be intellectually honest - acknowledge uncertainties
- Weight quantitative evidence (financials, metrics) heavily
- Consider both fundamental and sentiment factors
- Think like a professional investor, not a cheerleader
- If evidence is mixed or contradictory, reflect that in your conviction level
- Focus on risk-adjusted returns, not just potential upside

Use GPT-5 for the analytical synthesis, then hand off to Claude for writing the final verdict in a clear, professional format."""

        try:
            result = await runner.run(
                input=prompt,
                model=self.models,  # Will use model handoffs
                stream=False
            )

            return {
                "agent": "judge",
                "agent_name": self.name,
                "verdict": result.final_output,
                "status": "success",
                "stock_ticker": stock_ticker
            }

        except Exception as e:
            return {
                "agent": "judge",
                "agent_name": self.name,
                "verdict": f"Error during judgment: {str(e)}",
                "status": "error",
                "stock_ticker": stock_ticker
            }
