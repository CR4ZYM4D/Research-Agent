<div align="center">

```
██████╗ ███████╗███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
██████╔╝█████╗  ███████╗█████╗  ███████║██████╔╝██║     ███████║
██╔══██╗██╔══╝  ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
██║  ██║███████╗███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                    A G E N T
```

### *Autonomous Multi-Agent Research Intelligence*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Gemini_2.0_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/gemini)
[![Tavily](https://img.shields.io/badge/Tavily_Search-FF6B35?style=for-the-badge)](https://tavily.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-00E5FF?style=for-the-badge)](LICENSE)

<br/>

> **Four specialized AI agents. One research topic. One publication-quality report.**

</div>

---

## What This Does

ResearchAgent is a **multi-agent AI pipeline** that decomposes deep research into four specialized roles — searching, reading, writing, and critiquing — coordinated through a stateful LangChain pipeline, served via a FastAPI backend with a browser-based UI.

Give it any topic. Get back a structured, cited research report evaluated by an adversarial critic agent.

```
INPUT: "Recent advances in diffusion model architectures"
  │
  ├─► [SEARCHER]  Tavily deep search → 5 authoritative sources
  ├─► [READER]    Scrape highest-relevance URL → 4000 chars of content
  ├─► [WRITER]    Gemini 2.0 Flash → Intro + 3 Key Findings + Conclusion + Citations
  └─► [CRITIC]    Structured evaluation → Score / Strengths / Improvements / Verdict

OUTPUT: Structured report + score (X/10) + actionable critique
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      RESEARCH PIPELINE                          │
│                                                                 │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐   │
│   │ SEARCHER │───▶│  READER  │───▶│  WRITER  │───▶│ CRITIC  │   │
│   │  Agent   │    │  Agent   │    │  Chain   │    │  Chain  │   │
│   └──────────┘    └──────────┘    └──────────┘    └─────────┘   │
│        │               │               │               │        │
│   Tavily API      BeautifulSoup    Gemini 2.0       Gemini 2.0  │
│   5 sources       Full-page scrape Flash + Prompt   Flash + Eval│
│                                                                 │
│                    Shared State Dict                            │
│         search_results → reader_results → report → feedback     │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Tool | Responsibility | Output |
|---|---|---|---|
| **Searcher** | `TavilyClient` (depth=advanced) | Web-wide search, returns top-5 sources | Title + URL + 400-char snippets |
| **Reader** | `requests` + `BeautifulSoup` | Selects best URL, full-page scrape + clean | 4000 chars of structured text |
| **Writer** | `ChatGoogleGenerativeAI` (Gemini 2.0 Flash) | Synthesises Intro → Findings → Conclusion | Markdown report with citations |
| **Critic** | `ChatGoogleGenerativeAI` (Gemini 2.0 Flash) | Adversarial evaluation, structured scoring | Score/10 + Strengths + Improvements + Verdict |

### State Flow

```python
state = {}
state['search_results']  = searcher_agent.invoke(topic)      # Step 1
state['reader_results']  = reader_agent.invoke(search_top)   # Step 2
state['report']          = writer_chain.invoke(combined)     # Step 3
state['feedback']        = critic_chain.invoke(report)       # Step 4
```

---

## Tech Stack

```
┌─────────────────────────────────────────┐
│  LLM BACKBONE    │  Gemini 2.0 Flash    │
│  AGENT FRAMEWORK │  LangChain 0.2+      │
│  SEARCH          │  Tavily API (advanced)│
│  WEB SCRAPING    │  BeautifulSoup4 + lxml│
│  BACKEND         │  FastAPI + Uvicorn   │
│  VALIDATION      │  Pydantic v2         │
│  RESILIENCE      │  Tenacity (retries)  │
│  ASYNC           │  aiohttp             │
└─────────────────────────────────────────┘
```

---

## Project Structure

```
Research-Agent/
├── agents.py          # Searcher, Reader agents + Writer/Critic chains
├── tools.py           # web_search (Tavily) and scrape_url (BS4) tools
├── pipeline.py        # Stateful 4-step orchestration pipeline
├── server.py          # FastAPI backend — serves UI + /research endpoint
├── index.html         # Frontend UI (served at GET /)
├── requirements.txt   # Full dependency list
└── README.md
```

---

## Quickstart

### Prerequisites

- Python 3.10+
- A [Gemini API key](https://aistudio.google.com/app/apikey) (free tier works)
- A [Tavily API key](https://tavily.com) (free tier: 1000 searches/month)

### 1. Clone & Install

```bash
git clone https://github.com/CR4ZYM4D/Research-Agent.git
cd Research-Agent
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the repo root:

```env
GOOGLE_API_KEY=AIza...
TAVILY_API_KEY=tvly-...
```

> Keys can also be entered directly in the UI — they're stored in the browser session only.

### 3. Start the Server

```bash
uvicorn server:app --reload
```

Open `http://localhost:8000` in your browser. The UI loads, enter your topic, and the full pipeline runs.

### 4. Use Programmatically

```python
from pipeline import run_pipeline

state = run_pipeline("Recent advances in RAG pipeline optimization")

print(state['report'])    # Full research report
print(state['feedback'])  # Critic evaluation with score
```

---

## Output Format

### Report (Writer Agent)

```
## Introduction
[Context and scope of the research topic]

## Key Findings

**Finding 1 — [Theme]**
[Detailed, fact-based explanation with citations]

**Finding 2 — [Theme]**
...

**Finding 3 — [Theme]**
...

## Conclusion
[Synthesis and forward-looking insights]

## Sources
- https://source1.com
- https://source2.com
```

### Critique (Critic Agent)

```
Score: 8/10

Strengths:
- Well-structured with clear section hierarchy
- Three well-evidenced key findings with source attribution

Areas to Improve:
- More quantitative benchmarks would strengthen claims
- Deeper discussion of limitations and open problems

One line verdict: Strong, well-cited report — improve empirical depth for publication quality.
```

---

## Design Decisions

**Why Gemini 2.0 Flash?**
High throughput, low latency, strong instruction-following at temperature 0.5 — ideal for structured output tasks without overproduction.

**Why Tavily over Google Search API?**
Tavily's `search_depth=advanced` mode is purpose-built for LLM pipelines — clean structured results with no HTML boilerplate to parse.

**Why a stateful dict instead of LangGraph?**
This is intentionally minimal — a four-node linear DAG with no cycles or branching. A plain Python dict is simpler and faster for this use case. The architecture maps directly onto a LangGraph `StateGraph` if you want to extend it with conditional routing or memory.

---

## Extending the Pipeline

<details>
<summary><b>Add a Fact-Checker Agent</b></summary>

```python
# In agents.py
fact_check_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a rigorous fact-checker. Identify unverified claims."),
    ("human", "Report:\n{report}\n\nSources:\n{sources}\n\nList any claims that cannot be verified from the provided sources.")
])
fact_check_chain = fact_check_prompt | llm | StrOutputParser()
```

</details>

<details>
<summary><b>Migrate to LangGraph</b></summary>

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ResearchState(TypedDict):
    topic: str
    search_results: str
    reader_results: str
    report: str
    feedback: str

workflow = StateGraph(ResearchState)
workflow.add_node("search",   search_node)
workflow.add_node("read",     read_node)
workflow.add_node("write",    write_node)
workflow.add_node("critique", critique_node)
workflow.set_entry_point("search")
workflow.add_edge("search",   "read")
workflow.add_edge("read",     "write")
workflow.add_edge("write",    "critique")
workflow.add_edge("critique", END)

app = workflow.compile()
```

</details>

<details>
<summary><b>Add Conversation Memory</b></summary>

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
# Inject memory into each agent's invocation for multi-turn research sessions
```

</details>

---

## License

MIT — free to use, modify, and distribute. If you build something cool with it, a star is appreciated.

---

<div align="center">

*Built because everyone going insane over agents · Powered by Gemini + Tavily + LangChain*

</div>
