"""Financial Analysis Agent."""
from dataclasses import dataclass
import asyncio, json

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
        Perform comprehensive financial analysis of a stock using batched subtasks.
        """
        @dataclass
        class Subtask:
            name: str
            instruction: str
            timeout_s: int = 90

        subtasks = [
            Subtask("financial_health", "Evaluate the most recent 2025 liquidity, solvency, and key ratios (profit margin, ROE, ROA, debt-to-equity)."),
            Subtask("profitability", "Analyze the most recent 2025 revenue, net income, and margin trends over the past 3-5 years."),
            Subtask("valuation", "Compute or summarize the most recent 2025 valuation metrics (P/E, P/B, EV/EBITDA) and compare to peers."),
            Subtask("cash_flow", "Assess the most recent 2025 operating cash flow, free cash flow, and capex requirements."),
            Subtask("balance_sheet", "Review the most recent 2025 debt levels, cash reserves, and asset quality."),
        ]

        MICRO_PROMPT = """You are a financial analysis expert analyzing {ticker}.
    Task: {instruction}
    Return STRICT JSON:
    {{
    "summary": "≤120 words",
    "metrics": [{{"name": "string", "value": "string"}}],
    "strengths": ["string", ...],
    "weaknesses": ["string", ...],
    "stance": "BULLISH|BEARISH|NEUTRAL",
    "confidence": 0-10
    }}
    Only JSON. No prose outside the JSON.
    """

        async def run_subtask(runner, subtask):
            prompt = MICRO_PROMPT.format(ticker=stock_ticker, instruction=subtask.instruction)
            try:
                result = await asyncio.wait_for(
                    runner.run(
                        input=prompt,
                        model=self.model,
                        tools=self.tools,
                        mcp_servers=self.mcp_servers,
                        stream=False
                    ),
                    timeout=subtask.timeout_s
                )
                return json.loads(result.final_output)
            except Exception as e:
                return {"summary": f"{subtask.name} failed: {e}", "confidence": 0}

        # ---- Parallel map phase ----
        client = AsyncDedalus()
        runner = DedalusRunner(client)
        micro_results = await asyncio.gather(*[run_subtask(runner, s) for s in subtasks])

        # ---- Reduce phase ----
        reduce_prompt = f"""You are the financial judge synthesizing multiple partial analyses of {stock_ticker}.
    Input JSON list below. Summarize overlaps/conflicts and output final structured JSON:
    {{
    "overall_summary": "≤150 words",
    "key_strengths": ["≤5 bullets"],
    "key_weaknesses": ["≤5 bullets"],
    "overall_stance": "BULLISH|BEARISH|NEUTRAL",
    "confidence": 0-10
    }}
    Input:
    {json.dumps(micro_results, ensure_ascii=False)}
    Return only JSON.
    """

        try:
            reduce_result = await runner.run(
                input=reduce_prompt,
                model="openai/gpt-5",  # or self.model if preferred
                stream=False
            )
            final_json = json.loads(reduce_result.final_output)
            status = "success"
        except Exception as e:
            final_json = {"error": str(e), "partials": micro_results}
            status = "partial"

        return {
            "agent": "financial",
            "agent_name": self.name,
            "analysis": final_json,
            "status": status
        }

