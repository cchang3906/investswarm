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
        Run complete stock analysis with agent swarm.

        Args:
            stock_ticker: Stock ticker symbol (e.g., "TSLA", "AAPL")
            verbose: Whether to print progress updates

        Returns:
            Dictionary containing all analysis results and final verdict
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

            # Handle any exceptions from parallel execution
            final_results = []
            for i, result in enumerate(research_results):
                if isinstance(result, Exception):
                    agent_names = ["financial", "market", "sentiment"]
                    logger.error(f"Error in {agent_names[i]} agent: {str(result)}")
                    final_results.append({
                        "agent": agent_names[i],
                        "agent_name": f"{agent_names[i].title()} Agent",
                        "analysis": f"Error: {str(result)}",
                        "status": "error"
                    })
                else:
                    final_results.append(result)

        except Exception as e:
            logger.error(f"Critical error during research phase: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "stock_ticker": stock_ticker
            }

        if verbose:
            logger.info("\n" + "=" * 80)
            logger.info("Research phase complete. Starting judge agent...")
            logger.info("=" * 80 + "\n")

        # Phase 2: Run judge agent to synthesize and provide verdict
        try:
            verdict_result = await self._run_judge(final_results, stock_ticker, verbose)
        except Exception as e:
            logger.error(f"Error in judge agent: {str(e)}")
            verdict_result = {
                "agent": "judge",
                "verdict": f"Error: {str(e)}",
                "status": "error"
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
                "financial": final_results[0],
                "market": final_results[1],
                "sentiment": final_results[2],
            },
            "verdict": verdict_result,
        }

    async def _run_financial_analysis(self, stock_ticker: str, verbose: bool) -> Dict[str, Any]:
        """Run financial analysis agent."""
        if verbose:
            logger.info("[1/3] Financial Analysis Agent starting...")

        result = await self.financial_agent.analyze(stock_ticker)

        if verbose:
            status = "✓" if result["status"] == "success" else "✗"
            logger.info(f"[1/3] Financial Analysis Agent complete {status}\n")

        return result

    async def _run_market_analysis(self, stock_ticker: str, verbose: bool) -> Dict[str, Any]:
        """Run market analysis agent."""
        if verbose:
            logger.info("[2/3] Market & Product Analysis Agent starting...")

        result = await self.market_agent.analyze(stock_ticker)

        if verbose:
            status = "✓" if result["status"] == "success" else "✗"
            logger.info(f"[2/3] Market & Product Analysis Agent complete {status}\n")

        return result

    async def _run_sentiment_analysis(self, stock_ticker: str, verbose: bool) -> Dict[str, Any]:
        """Run sentiment analysis agent."""
        if verbose:
            logger.info("[3/3] Sentiment Analysis Agent starting...")

        result = await self.sentiment_agent.analyze(stock_ticker)

        if verbose:
            status = "✓" if result["status"] == "success" else "✗"
            logger.info(f"[3/3] Sentiment Analysis Agent complete {status}\n")

        return result

    async def _run_judge(
        self,
        research_results: List[Dict[str, Any]],
        stock_ticker: str,
        verbose: bool
    ) -> Dict[str, Any]:
        """Run judge agent to provide final verdict."""
        if verbose:
            logger.info("Judge Agent evaluating research and formulating verdict...")

        result = await self.judge_agent.judge(research_results, stock_ticker)

        if verbose:
            status = "✓" if result["status"] == "success" else "✗"
            logger.info(f"Judge Agent complete {status}\n")

        return result


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
