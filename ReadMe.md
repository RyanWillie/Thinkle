# 🧠 TheThinkle.ai

**TheThinkle.ai** is a personalized, autonomous research assistant that delivers a weekly (or optionally daily) TL;DR-style newsletter — entertaining, insightful, and tailored to your interests.

It scouts the digital world, filters for signal over noise, performs deep dives on important topics, and presents the result as a smart, witty newsletter you’ll actually want to read.

---

## �� Key Features

* 🧠 **Dynamic Personalization**: Define your interests (`AI`, `geopolitics`, `biotech`, etc.) and let Thinkle do the rest.
* 🔍 **Autonomous Research Pipeline**: Uses search APIs, web scraping, Reddit, YouTube, and ArXiv tools to find stories worth telling.
* ✍️ **Newsletter Generation**: Outputs a markdown and/or PDF newsletter with summaries, opinions, source links, and "dig deeper" sections.
* 🎨 **Optional Image Generation**: Generates a header image for each newsletter issue.
* 💬 **Opinionated (if you want)**: Adds clearly-marked hot takes next to objective summaries.
* 🛠️ **Modular Langchain Agents**: Built using agents + tools + chains, completely customizable and local-first.

---

## 🧱 Project Structure

```
thethinkle/
🔹 agents/                # Decision-making LLM agents
🔹 tools/                 # Source scrapers and search wrappers
🔹 chains/                # Reusable LLM chains (summarize, opinion, cite)
🔹 composer/              # Newsletter formatting & output
🔹 config/                # User preferences and prompts
🔹 data/                  # Raw input + generated outputs
🔹 utils/                 # Helper utilities
🔹 generate_newsletter.py # Main CLI trigger
🔹 requirements.txt
🔹 .env                   # API keys (excluded from version control)
🔹 README.md
```

---

## 🧠 How It Works

1. **Input Interests**

   * You define your interests in `config/interests.yaml`.

2. **Trigger Execution**

   * Run `python generate_newsletter.py` to kick off the pipeline.

3. **Planning Agent**

   * Uses search tools and topic agents to gather new, relevant information.
   * Filters out noise, ranks top stories.

4. **Deep Investigation**

   * For selected items, issues follow-up queries and gathers contextual information from multiple viewpoints.

5. **Content Composition**

   * Produces a concise summary with optional opinion and citations.
   * Generates a markdown or PDF newsletter.

6. **Final Output**

   * Located in `data/outputs/` — clean, verified, and easily digestible.

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/thethinkle.git
cd thethinkle
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your Interests

Edit `config/interests.yaml`:

```yaml
interests:
  - ai
  - geopolitics
  - biotech
tone: witty
opinion: true
```

### 4. Set API Keys

Create a `.env` file:

```
SERPAPI_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### 5. Generate Your First Newsletter

```bash
python generate_newsletter.py
```

Output will be saved to `data/outputs/`.

---

## 🧩 Roadmap

* [ ] Scheduler support for weekly and daily runs
* [ ] Email delivery integration
* [ ] Feedback + learning loop (like/dislike stories)
* [ ] Local LLM + embedding support (e.g., GPT4All, Ollama)
* [ ] Multi-user / web dashboard

---

## 📜 License

MIT – Use it, remix it, just don't gatekeep the good stuff.

---

## 🙌 Acknowledgements

Built with:

* [Langchain](https://github.com/langchain-ai/langchain)
* [OpenAI](https://platform.openai.com/)
* [SerpAPI](https://serpapi.com/)
* [PRAW](https://praw.readthedocs.io/en/stable/) (Reddit)
* [ArXiv API](https://arxiv.org/help/api/index)
* [Mermaid](https://mermaid.js.org/) for architecture diagrams

---

> “Don’t scroll. Thinkle.” 🧠✨

