# 🧠 TheThinkle.ai

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![LangGraph](https://img.shields.io/badge/LangGraph-Powered-green.svg)](https://github.com/langchain-ai/langgraph)

**TheThinkle.ai** is a personalized, autonomous research assistant that delivers a weekly (or optionally daily) TL;DR-style newsletter — entertaining, insightful, and tailored to your interests.

It scouts the digital world, filters for signal over noise, performs deep dives on important topics, and presents the result as a smart, witty newsletter you'll actually want to read.

---

## ✨ Key Features

* 🧠 **Dynamic Personalization**: Define your interests (`AI`, `geopolitics`, `biotech`, etc.) and let Thinkle do the rest.
* 🔍 **Autonomous Research Pipeline**: Uses search APIs, web scraping, Reddit, YouTube, and ArXiv tools to find stories worth telling.
* ✍️ **Newsletter Generation**: Outputs a markdown newsletter with summaries, opinions, source links, and "dig deeper" sections.
* 💬 **Opinionated (if you want)**: Adds clearly-marked hot takes next to objective summaries.
* 🛠️ **LangGraph-Powered Agents**: Built using LangGraph's agent orchestration framework for reliable, stateful workflows.
* 🔬 **LangGraph Studio Integration**: Debug and visualize your agent workflows in real-time.

---

## 🧱 Project Structure

```
thethinkle/
├── agents/                 # Decision-making LLM agents
│   ├── planner.py         # Plans research tasks based on interests
│   ├── scout.py           # Executes research and gathers information
│   ├── evaluator.py       # Evaluates and scores content relevance
│   ├── writer.py          # Composes the final newsletter
│   └── states.py          # Shared state definitions for agents
├── tools/                  # External data source integrations
│   └── basic_tools.py     # Search, web scraping, and API wrappers
├── prompts/                # LLM prompts and templates
│   └── prompts.py         # Centralized prompt management
├── config/                 # Configuration management
│   ├── config_parser.py   # Configuration loading and validation
│   └── interests.yaml     # User interests and preferences
├── data/                   # Pipeline outputs
│   └── outputs/           # Generated newsletters
├── tests/                  # Test suite
│   ├── unit/              # Unit tests for individual components
│   ├── integration/       # End-to-end pipeline tests
│   └── fixtures/          # Test data and fixtures
├── studio/                 # LangGraph Studio configuration
│   ├── app.py             # Studio entry point
│   └── langgraph.json     # Studio configuration
├── generate_newsletter.py  # Main CLI entry point
├── langgraph.json         # LangGraph configuration
├── requirements.txt       # Python dependencies
├── Makefile              # Development commands
├── pytest.ini            # Pytest configuration
├── .env                  # API keys (excluded from version control)
└── README.md
```

---

## 🧠 How It Works

The newsletter generation pipeline uses a multi-agent workflow orchestrated by LangGraph:

1. **Planner Agent**
   * Reads your interests from `config/interests.yaml`
   * Generates targeted research tasks for each topic
   * Creates a plan for the newsletter structure

2. **Scout Agent** (Parallel Execution)
   * Executes research tasks concurrently
   * Queries search engines, Reddit, ArXiv, YouTube, and news sources
   * Gathers raw content and metadata from multiple viewpoints

3. **Evaluator Agent**
   * Scores and ranks content based on relevance, recency, and quality
   * Filters out noise and low-quality information
   * Uses your user profile to personalize scoring

4. **Writer Agent**
   * Composes a cohesive newsletter from top stories
   * Adds summaries, opinions (if enabled), and source citations
   * Formats the output as markdown

5. **Final Output**
   * Located in `data/outputs/newsletter-YYYYMMDD-HHMMSS.md`
   * Clean, verified, and easily digestible

---

## 🚀 Getting Started

### Prerequisites

* Python 3.11 or higher
* OpenAI API key
* LangSmith API key (optional, for tracing)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Thinkle.git
cd Thinkle
```

### 2. Set Up Python Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
# Or use make
make install
```

### 4. Configure Your Interests

Edit `config/interests.yaml`:

```yaml
# Core interests - topics you want to stay updated on
interests:
  - artificial intelligence
  - machine learning
  - geopolitics
  - space exploration

# Brief user background used to tailor scoring, tone, and relevance
user_profile: "Ryan is a 25 year old Australian male, he currently works as a software engineer in the UK."

# Newsletter preferences
newsletter:
  tone: "witty"              # Options: professional, witty, casual, academic
  include_opinions: true     # Include AI-generated opinions and hot takes
  frequency: "weekly"        # Options: daily, weekly
  max_stories: 10           # Maximum number of stories per newsletter

# Model configuration
models:
  planner: "gpt-5"
  scout: "gpt-5-mini"
  evaluator: "gpt-5"
  writer: "gpt-5"

max_tasks: 3
```

### 5. Set API Keys

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional for tracing
```

### 6. Generate Your First Newsletter

```bash
python generate_newsletter.py

# Or with custom config
python generate_newsletter.py --config config/interests.yaml

# Verbose logging
python generate_newsletter.py --verbose
```

Output will be saved to `data/outputs/newsletter-YYYYMMDD-HHMMSS.md`.

---

## 🛠️ Development

### Using the Makefile

The project includes a comprehensive Makefile for common development tasks:

```bash
# Run all tests
make test

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run tests with coverage
make test-coverage

# Format code with Black
make format

# Lint code with flake8
make lint

# Full development cycle (format, lint, test)
make dev

# Launch LangGraph Studio for debugging
make studio
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_config_parser.py

# Run with verbose output
pytest -v -s

# Run with coverage
pytest --cov=. --cov-report=html
```

### LangGraph Studio

Debug and visualize your agent workflows in real-time:

```bash
make studio
# Or directly:
langgraph dev
```

This launches an interactive web UI where you can:
* Step through agent execution
* Inspect state at each node
* Modify inputs and re-run
* Visualize the graph structure

---

## 🧪 Code Quality

The project follows these standards:

* **Formatting**: Black (88 characters, 4-space indent)
* **Linting**: Flake8
* **Type Hints**: Required for all functions
* **Testing**: Pytest with fixtures
* **Docstrings**: Google-style for all modules and classes

```bash
# Format code
black .

# Check formatting
black --check --diff .

# Lint code
flake8 .

# Validate configuration
python -c "from config import load_config; config = load_config(); print('✅ Configuration is valid!')"
```

---

## 📦 Dependencies

### Core Framework
* **LangChain 0.3.x** - LLM framework
* **LangGraph** - Agent orchestration and state management
* **OpenAI 1.104+** - LLM provider
* **Pydantic 2.8+** - Data validation

### Data Sources
* **PRAW** - Reddit API
* **ArXiv API** - Academic papers
* **youtube-transcript-api** - YouTube transcripts
* **googlesearch-python** - Web search
* **duckduckgo-search** - Alternative search
* **BeautifulSoup4** - Web scraping

### Output & Utilities
* **python-dotenv** - Environment management
* **PyYAML** - Configuration files
* **Jinja2** - Template engine
* **pytest** - Testing framework

See `requirements.txt` for the complete list.

---

## 📁 Configuration Reference

### interests.yaml Structure

```yaml
interests:              # List of topics to research
  - topic1
  - topic2

user_profile:          # Brief user background for personalization

newsletter:
  tone:                # professional | witty | casual | academic
  include_opinions:    # true | false
  frequency:           # daily | weekly
  max_stories:         # integer

content:
  include_academic:    # Include ArXiv papers
  include_reddit:      # Include Reddit discussions
  include_youtube:     # Include YouTube content
  include_news:        # Include news articles

output:
  format:              # markdown | pdf | html
  include_sources:     # true | false
  include_summary_stats: # true | false

models:
  planner:             # Model for planner agent
  scout:               # Model for scout agent
  evaluator:           # Model for evaluator agent
  writer:              # Model for writer agent

max_tasks:             # Max parallel research tasks
```

---

## 🧩 Roadmap

* [x] LangGraph-based agent orchestration
* [x] Multi-agent research pipeline
* [x] Configurable interests and preferences
* [x] LangGraph Studio integration
* [x] Comprehensive test suite
* [ ] Scheduler support for automated runs
* [ ] Email delivery integration
* [ ] Feedback loop (like/dislike stories)
* [ ] Local LLM support (Ollama, GPT4All)
* [ ] PDF output generation
* [ ] Web dashboard
* [ ] Multi-user support

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Make your changes following the coding standards
4. Run tests and linting (`make dev`)
5. Commit using Conventional Commits format
6. Push to your branch and open a Pull Request

---

## 📜 License

MIT – Use it, remix it, just don't gatekeep the good stuff.

---

## 🙌 Acknowledgements

Built with:

* [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
* [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
* [OpenAI](https://platform.openai.com/) - LLM provider
* [PRAW](https://praw.readthedocs.io/en/stable/) - Reddit API wrapper
* [ArXiv API](https://arxiv.org/help/api/index) - Academic paper access
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Web scraping
* [Pytest](https://pytest.org/) - Testing framework

---

## 📚 Additional Resources

* [AGENTS.md](AGENTS.md) - Detailed agent architecture documentation
* [tests/README.md](tests/README.md) - Testing guidelines
* [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
* [LangSmith Tracing](https://docs.smith.langchain.com/)

---

> "Don't scroll. Thinkle." 🧠✨