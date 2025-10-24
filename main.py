#!/usr/bin/env python3
"""
InvestSwarm - AI Agent Swarm for Stock Analysis

A multi-agent system that analyzes stocks from three different perspectives:
- Financial Analysis
- Market & Product Analysis
- Sentiment Analysis

Then conducts a debate judged by a final LLM that gives the verdict.
"""

import asyncio
import argparse
import sys
import json
from datetime import datetime

from src.swarm import analyze_stock
from src.utils.logger import logger


def print_banner():
    """Print InvestSwarm banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║                      INVESTSWARM                          ║
    ║              AI Agent Swarm for Stock Analysis            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_verdict(verdict_data: dict):
    """
    Print the final verdict in a formatted way.

    Args:
        verdict_data: Verdict dictionary from judge agent
    """
    print("\n" + "=" * 80)
    print("FINAL VERDICT")
    print("=" * 80 + "\n")

    if verdict_data["status"] == "success":
        print(verdict_data["verdict"])
    else:
        print(f"Error: {verdict_data.get('verdict', 'Unknown error')}")

    print("\n" + "=" * 80)


def print_research_summary(research_data: dict):
    """
    Print a summary of each agent's research.

    Args:
        research_data: Research dictionary containing all agent analyses
    """
    print("\n" + "=" * 80)
    print("RESEARCH SUMMARY")
    print("=" * 80 + "\n")

    for agent_type in ["financial", "market", "sentiment"]:
        agent_result = research_data.get(agent_type, {})
        agent_name = agent_result.get("agent_name", agent_type.title())
        status = agent_result.get("status", "unknown")

        print(f"\n--- {agent_name} ---")
        print(f"Status: {status.upper()}")

        if status == "success":
            analysis = agent_result.get("analysis", "No analysis available")
            # Print first 500 characters as preview
            preview = analysis[:500] + "..." if len(analysis) > 500 else analysis
            print(f"\nPreview:\n{preview}\n")
        else:
            print(f"Error: {agent_result.get('analysis', 'Unknown error')}\n")

    print("=" * 80)


def save_results(results: dict, output_file: str):
    """
    Save results to JSON file.

    Args:
        results: Complete results dictionary
        output_file: Path to output file
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"\nResults saved to: {output_file}")
    except Exception as e:
        logger.error(f"Failed to save results: {str(e)}")


async def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="InvestSwarm - AI Agent Swarm for Stock Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py TSLA                    # Analyze Tesla stock
  python main.py AAPL -o results.json    # Analyze Apple and save to file
  python main.py MSFT --show-research    # Show detailed research from all agents
  python main.py NVDA -q                 # Quiet mode, only show verdict

For more information, visit: https://github.com/yourusername/investswarm
        """
    )

    parser.add_argument(
        "ticker",
        type=str,
        help="Stock ticker symbol (e.g., TSLA, AAPL, MSFT)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Save complete results to JSON file"
    )

    parser.add_argument(
        "--show-research",
        action="store_true",
        help="Show detailed research from all agents"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode - only show final verdict"
    )

    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Don't show the banner"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="InvestSwarm 0.1.0"
    )

    args = parser.parse_args()

    # Print banner
    if not args.no_banner and not args.quiet:
        print_banner()

    # Validate ticker
    ticker = args.ticker.upper()
    if not ticker.isalnum() or len(ticker) > 5:
        logger.error("Invalid ticker symbol. Please use 1-5 alphanumeric characters.")
        sys.exit(1)

    # Run analysis
    try:
        verbose = not args.quiet
        results = await analyze_stock(ticker, verbose=verbose)

        # Show research summary if requested
        if args.show_research and not args.quiet:
            print_research_summary(results["research"])

        # Always show verdict
        print_verdict(results["verdict"])

        # Save to file if requested
        if args.output:
            save_results(results, args.output)

        # Exit with appropriate code
        if results["status"] == "success":
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("\n\nAnalysis interrupted by user.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\nFatal error: {str(e)}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
