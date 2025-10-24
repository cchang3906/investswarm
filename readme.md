# InvestSwarm

**AI Agent Swarm for Stock Analysis**

InvestSwarm is a multi-agent system powered by [Dedalus Labs](https://dedaluslabs.ai) that analyzes stocks from three different perspectives in parallel, then synthesizes the research through a debate judged by a final LLM.

## Overview

InvestSwarm uses **four specialized AI agents**:

1. **Financial Analysis Agent** - Analyzes financial statements, ratios, profitability, cash flow, and balance sheet strength
2. **Market & Product Analysis Agent** - Evaluates market position, competitive landscape, product strength, and economic moat
3. **Sentiment Analysis Agent** - Assesses news sentiment, analyst ratings, social media, and insider activity
4. **Judge Agent** - Synthesizes all research, identifies agreements/conflicts, and provides a final investment verdict

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input: Stock Ticker                  │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────────┐ ┌────────────┐ ┌────────────────┐
│   Financial    │ │   Market   │ │   Sentiment    │
│    Analysis    │ │  Analysis  │ │    Analysis    │
│     Agent      │ │   Agent    │ │     Agent      │
└────────┬───────┘ └──────┬─────┘ └────────┬───────┘
         │                │                 │
         └────────────────┼─────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Judge Agent   │
                  │ (Synthesizes  │
                  │  & Decides)   │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Final Verdict │
                  │ BUY/HOLD/SELL │
                  └───────────────┘
```

## Features

- **Parallel Processing**: Three agents research simultaneously for faster results
- **Multi-Model Support**: Uses GPT-5 for analysis and Claude for verdict writing (model handoffs)
- **Comprehensive Analysis**: Combines fundamental, market, and sentiment factors
- **MCP Integration**: Leverages Brave Search and Exa for real-time data
- **Custom Tools**: Financial ratio calculators, sentiment scoring, code execution
- **CLI Interface**: Easy-to-use command-line interface
- **JSON Export**: Save complete results for further analysis

## Installation

### Prerequisites

- Python 3.8 or higher
- Dedalus API key (get one at [dedaluslabs.ai](https://dedaluslabs.ai))

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/investswarm.git
   cd investswarm
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Dedalus API key:
   ```bash
   DEDALUS_API_KEY=your_api_key_here
   ```

   > **Note**: You only need a `DEDALUS_API_KEY`. Dedalus handles routing to all model providers (OpenAI, Anthropic, etc.) for you. Optionally, you can bring your own API keys for specific providers.

## Usage

### Basic Usage

Analyze a stock by ticker symbol:

```bash
python main.py TSLA
```

This will:
1. Run three agents in parallel to research Tesla
2. Display progress updates
3. Show the final investment verdict

### Command-Line Options

```bash
python main.py <ticker> [options]

Options:
  -o, --output FILE       Save complete results to JSON file
  --show-research         Show detailed research from all agents
  -q, --quiet            Quiet mode - only show final verdict
  --no-banner            Don't show the banner
  --version              Show version number
  -h, --help             Show help message
```

### Examples

**Analyze Apple stock**:
```bash
python main.py AAPL
```

**Save results to file**:
```bash
python main.py MSFT -o results.json
```

**Show detailed research from all agents**:
```bash
python main.py NVDA --show-research
```

**Quiet mode (verdict only)**:
```bash
python main.py GOOGL -q
```

### Using as a Library

You can also use InvestSwarm programmatically:

```python
import asyncio
from src.swarm import analyze_stock

async def main():
    # Analyze a stock
    results = await analyze_stock("TSLA", verbose=True)

    # Access the verdict
    print(results["verdict"]["verdict"])

    # Access individual agent analyses
    financial_analysis = results["research"]["financial"]["analysis"]
    market_analysis = results["research"]["market"]["analysis"]
    sentiment_analysis = results["research"]["sentiment"]["analysis"]

if __name__ == "__main__":
    asyncio.run(main())
```

## Output Format

### Console Output

InvestSwarm provides clear, structured output:

```
╔═══════════════════════════════════════════════════════════╗
║                      INVESTSWARM                          ║
║              AI Agent Swarm for Stock Analysis            ║
╚═══════════════════════════════════════════════════════════╝

Starting parallel research with 3 specialized agents...

[1/3] Financial Analysis Agent starting...
[2/3] Market & Product Analysis Agent starting...
[3/3] Sentiment Analysis Agent starting...

[Agents complete their research...]

================================================================================
FINAL VERDICT
================================================================================

Investment Recommendation: BUY
Conviction Level: 8/10

[Detailed analysis and reasoning...]
```

### JSON Output

When using `-o` flag, results are saved in this structure:

```json
{
  "status": "success",
  "stock_ticker": "TSLA",
  "timestamp": "2025-10-24T12:00:00",
  "duration_seconds": 45.2,
  "research": {
    "financial": {
      "agent": "financial",
      "agent_name": "Financial Analysis Agent",
      "analysis": "...",
      "status": "success"
    },
    "market": { ... },
    "sentiment": { ... }
  },
  "verdict": {
    "agent": "judge",
    "verdict": "...",
    "status": "success"
  }
}
```

## Architecture

### Project Structure

```
investswarm/
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── README.md                    # This file
├── knowledge_base/              # Documentation
│   └── dedalus-llms-full.txt   # Dedalus SDK docs
└── src/
    ├── __init__.py             # Package initialization
    ├── config.py               # Configuration management
    ├── swarm.py                # Main orchestration
    ├── agents/                 # Agent implementations
    │   ├── __init__.py
    │   ├── financial_agent.py  # Financial analysis
    │   ├── market_agent.py     # Market analysis
    │   ├── sentiment_agent.py  # Sentiment analysis
    │   └── judge_agent.py      # Judge/verdict
    ├── tools/                  # Custom tools
    │   ├── __init__.py
    │   ├── financial_tools.py  # Financial calculators
    │   ├── sentiment_tools.py  # Sentiment scoring
    │   └── code_execution.py   # Safe code execution
    └── utils/                  # Utilities
        ├── __init__.py
        └── logger.py           # Logging
```

### Agent Details

#### Financial Analysis Agent
- **Model**: GPT-5
- **MCP Servers**: Brave Search
- **Tools**: Financial ratio calculators, valuation metrics, growth analysis, Python code execution
- **Focus**: Balance sheets, income statements, cash flow, profitability, debt levels

#### Market & Product Analysis Agent
- **Model**: GPT-5
- **MCP Servers**: Brave Search, Exa (semantic search)
- **Tools**: Web search for market research
- **Focus**: Market size, competitive landscape, product differentiation, economic moat

#### Sentiment Analysis Agent
- **Model**: GPT-5
- **MCP Servers**: Brave Search, Exa
- **Tools**: Sentiment scoring, news aggregation
- **Focus**: News sentiment, analyst ratings, social media, insider activity

#### Judge Agent
- **Models**: GPT-5 → Claude Sonnet (handoff)
- **Process**: Synthesizes research, identifies conflicts, weighs evidence, provides verdict
- **Output**: BUY/HOLD/SELL recommendation with confidence level

## Configuration

Edit `src/config.py` to customize:

- Model selection for each agent
- MCP servers to use
- Agent prompts and behavior
- Tool availability

## Development

### Running Tests

```bash
# Coming soon
pytest tests/
```

### Adding New Agents

Create a new agent class in `src/agents/`:

```python
from dedalus_labs import AsyncDedalus, DedalusRunner

class YourAgent:
    def __init__(self):
        self.name = "Your Agent"
        self.model = "openai/gpt-5"

    async def analyze(self, stock_ticker: str):
        # Your analysis logic
        pass
```

### Adding Custom Tools

Add tools in `src/tools/` and register them with your agent:

```python
def your_custom_tool(arg1: str, arg2: int) -> str:
    """Tool description."""
    # Implementation
    return result
```

## MCP Servers Used

- **[windsor/brave-search-mcp](https://dedaluslabs.ai)**: Real-time web search for current data
- **[joerup/exa-mcp](https://dedaluslabs.ai)**: Semantic search for deep research

## Limitations & Disclaimers

⚠️ **IMPORTANT DISCLAIMERS**:

- **Not Financial Advice**: InvestSwarm is for educational and research purposes only. It does NOT provide financial advice.
- **Do Your Own Research**: Always conduct your own due diligence before making investment decisions.
- **No Guarantees**: AI analysis can be wrong. Markets are unpredictable.
- **Data Freshness**: Analysis depends on publicly available data, which may be outdated or incomplete.
- **API Costs**: Running InvestSwarm consumes Dedalus API credits.

## Roadmap

- [ ] Add more specialized agents (technical analysis, options flow, etc.)
- [ ] Support for multiple stocks comparison
- [ ] Historical analysis and backtesting
- [ ] Integration with portfolio management
- [ ] Web dashboard for results visualization
- [ ] Real-time monitoring and alerts
- [ ] Custom MCP server for financial APIs

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Dedalus Labs](https://dedaluslabs.ai) SDK
- Powered by OpenAI GPT-5 and Anthropic Claude
- MCP servers by Windsor and Joerup

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/investswarm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/investswarm/discussions)
- **Dedalus Support**: [Discord](https://discord.gg/K3SjuFXZJw)

---

**Made with ❤️ by the InvestSwarm team**

*Disclaimer: This software is for educational purposes only. Always consult with a qualified financial advisor before making investment decisions.*
