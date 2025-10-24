"""Main orchestration for InvestSwarm."""

import asyncio
from typing import Dict, Any, List
from datetime import datetime

from .agents import FinancialAgent, MarketAgent, SentimentAgent, JudgeAgent
from .utils.logger import logger


class InvestSwarm:
    """Orchestrates the multi-agent stock analysis system."""

    def __init__(self):
        self.financial_agent = FinancialAgent()
        self.market_agent = MarketAgent()
        self.sentiment_agent = SentimentAgent()
        self.judge_agent = JudgeAgent()

    async def analyze_stock(self, stock_ticker: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Run stock analysis with ALL THREE research agents (financial, market, sentiment)
    and SKIP the judge. The final 'verdict' will simply concatenate each agent's
    output so the CLI prints them after completion.
    """
    start_time = datetime.now()
    stock_ticker = stock_ticker.upper()

    if verbose:
        logger.info(f"\n{'=' * 80}")
        logger.info(f"InvestSwarm Analysis: {stock_ticker}")
        logger.info(f"{'=' * 80}\n")
        logger.info("Starting parallel research with 3 specialized agents...\n")

    # Phase 1: Run research agents in parallel
    try:
        research_results = await asyncio.gather(
            self._run_financial_analysis(stock_ticker, verbose),
            self._run_market_analysis(stock_ticker, verbose),
            self._run_sentiment_analysis(stock_ticker, verbose),
            return_exceptions=True
        )

        keys_in_order = [
            ("financial", "Financial Analysis Agent"),
            ("market", "Market & Product Analysis Agent"),
            ("sentiment", "Sentiment Analysis Agent"),
        ]

        results_map: Dict[str, Dict[str, Any]] = {}
        for (key, pretty), result in zip(keys_in_order, research_results):
            if isinstance(result, Exception):
                logger.error(f"Error in {key} agent: {str(result)}")
                results_map[key] = {
                    "agent": key,
                    "agent_name": pretty,
                    "analysis": f"Error: {str(result)}",
                    "status": "error",
                }
            else:
                results_map[key] = result

    except Exception as e:
        logger.error(f"Critical error during research phase: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "stock_ticker": stock_ticker,
        }

    if verbose:
        logger.info("\n" + "=" * 80)
        logger.info("All agents complete. Printing outputs (no judge)...")
        logger.info("=" * 80 + "\n")

    # Phase 2: NO JUDGE — build a printable “verdict” by concatenating each agent's output
    import json as _json

    def _as_text(analysis: Any) -> str:
        if isinstance(analysis, dict):
            return _json.dumps(analysis, indent=2, ensure_ascii=False)
        return str(analysis)

    combined_text_parts = []
    for key, pretty in keys_in_order:
        agent_res = results_map.get(key, {})
        analysis = agent_res.get("analysis", "No analysis available")
        combined_text_parts.append(
            f"{'=' * 80}\n{pretty.upper()}\n{'=' * 80}\n\n{_as_text(analysis)}\n"
        )
    combined_text = "\n".join(combined_text_parts)

    verdict_result = {
        "agent": "judge",  # keep the existing CLI shape
        "agent_name": "Agent Outputs (No Judge)",
        "verdict": combined_text,
        "status": "success",
        "stock_ticker": stock_ticker,
    }

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    if verbose:
        logger.info("\n" + "=" * 80)
        logger.info(f"Analysis complete in {duration:.2f} seconds")
        logger.info("=" * 80 + "\n")

    # Compile final output
    return {
        "status": "success",
        "stock_ticker": stock_ticker,
        "timestamp": start_time.isoformat(),
        "duration_seconds": duration,
        "research": {
            "financial": results_map["financial"],
            "market": results_map["market"],
            "sentiment": results_map["sentiment"],
        },
        "verdict": verdict_result,
    }



async def analyze_stock(stock_ticker: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Convenience function to analyze a stock.

    Args:
        stock_ticker: Stock ticker symbol
        verbose: Whether to print progress updates

    Returns:
        Analysis results and verdict
    """
    swarm = InvestSwarm()
    return await swarm.analyze_stock(stock_ticker, verbose)
