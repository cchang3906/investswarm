#!/usr/bin/env python3
"""
Example usage of InvestSwarm as a library.

This demonstrates how to use InvestSwarm programmatically
rather than through the CLI.
"""

import asyncio
import json
from src.swarm import analyze_stock


async def example_basic():
    """analyze a single stock."""
    print("=" * 80)
    print("Example 1: Basic Stock Analysis")
    print("=" * 80 + "\n")

    # Analyze Tesla
    results = await analyze_stock("TSLA", verbose=True)

    # Print the verdict
    print("\nFinal Verdict:")
    print(results["verdict"]["verdict"])


async def example_multiple_stocks():
    """Analyze multiple stocks in sequence."""
    print("\n" + "=" * 80)
    print("Example 2: Multiple Stock Analysis")
    print("=" * 80 + "\n")

    tickers = ["AAPL", "MSFT", "GOOGL"]

    for ticker in tickers:
        print(f"\nAnalyzing {ticker}...")
        results = await analyze_stock(ticker, verbose=False)

        # Extract key info
        verdict = results["verdict"]
        if verdict["status"] == "success":
            # Simple parsing - in production you'd want more robust extraction
            verdict_text = verdict["verdict"]
            print(f"\n{ticker} Analysis Complete:")
            print(f"Status: {verdict['status']}")
            print(f"Preview: {verdict_text[:200]}...")
        else:
            print(f"{ticker} Error: {verdict.get('verdict', 'Unknown error')}")


async def example_custom_processing():
    """Example with custom post-processing of results."""
    print("\n" + "=" * 80)
    print("Example 3: Custom Processing")
    print("=" * 80 + "\n")

    # Analyze a stock
    results = await analyze_stock("NVDA", verbose=True)

    # Extract and process data
    if results["status"] == "success":
        # Get each agent's analysis
        financial = results["research"]["financial"]["analysis"]
        market = results["research"]["market"]["analysis"]
        sentiment = results["research"]["sentiment"]["analysis"]

        # Custom processing
        summary = {
            "ticker": results["stock_ticker"],
            "timestamp": results["timestamp"],
            "duration": results["duration_seconds"],
            "agents": {
                "financial": {
                    "status": results["research"]["financial"]["status"],
                    "length": len(financial)
                },
                "market": {
                    "status": results["research"]["market"]["status"],
                    "length": len(market)
                },
                "sentiment": {
                    "status": results["research"]["sentiment"]["status"],
                    "length": len(sentiment)
                }
            },
            "verdict_status": results["verdict"]["status"]
        }

        print("\nProcessed Summary:")
        print(json.dumps(summary, indent=2))

        # Save to file
        output_file = f"analysis_{results['stock_ticker']}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nFull results saved to: {output_file}")


async def main():
    """Run all examples."""
    # Choose which example to run
    print("InvestSwarm Examples\n")
    print("Choose an example:")
    print("1. Basic stock analysis (TSLA)")
    print("2. Multiple stocks analysis")
    print("3. Custom processing (NVDA)")
    print("4. Run all examples")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        await example_basic()
    elif choice == "2":
        await example_multiple_stocks()
    elif choice == "3":
        await example_custom_processing()
    elif choice == "4":
        await example_basic()
        await example_multiple_stocks()
        await example_custom_processing()
    else:
        print("Invalid choice. Running basic example...")
        await example_basic()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
