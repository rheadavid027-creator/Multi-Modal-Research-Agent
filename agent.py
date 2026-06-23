from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

# ──────────────────────────────────────────────
# 1. LLMs
# ──────────────────────────────────────────────
groq_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
mistral_llm = ChatMistralAI(model="mistral-medium-latest", temperature=0.3)

# ──────────────────────────────────────────────
# 2. Tool Runner — manually invoke tools, collect raw data string
# ──────────────────────────────────────────────
def collect_raw_data(topic: str) -> str:
    """Call tools directly and concatenate results into one string."""
    results = []

    try:
        web_result = web_search.invoke({"query": topic})
        results.append(f"## Web Search Results\n{web_result}")
    except Exception as e:
        results.append(f"## Web Search Results\nError: {e}")

    def get_first_url(text: str):
        for line in text.splitlines():
            if line.strip().startswith("URL:"):
                return line.split("URL:", 1)[1].strip()
        return None

    try:
        first_url = get_first_url(web_result)
        if first_url:
            paper_result = scrape_url.invoke({"url": first_url})
            results.append(f"## Web Page Analysis\n{paper_result}")
        else:
            results.append("## Web Page Analysis\nNo valid URL found to scrape from search results.")
    except Exception as e:
        results.append(f"## Web Page Analysis\nError: {e}")

    return "\n\n".join(results)

# ──────────────────────────────────────────────
# 3. AGENT 1 — Researcher (Groq / LLaMA-3)
#    Summarizes the raw tool data
# ──────────────────────────────────────────────
researcher_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a research data collector. Your job is to:
1. Summarize key facts, findings, methodologies, and results from the given raw data
2. Return a clean structured summary with sources

Format your output as:
## Web Findings
...
## Academic Papers
...
## Key Facts & Data Points
...
"""),
    ("human", "Topic: {topic}\n\nRaw Data:\n{raw_data}"),
])

researcher_chain = researcher_prompt | groq_llm | StrOutputParser()

# ──────────────────────────────────────────────
# 4. AGENT 2 — Analyst (Mistral)
#    Deep analysis of researcher summary
# ──────────────────────────────────────────────
analyst_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a critical research analyst. Given research summaries, you must:
1. Identify core themes and arguments
2. Compare different sources and approaches
3. Spot contradictions, gaps, or open problems
4. Synthesize into a coherent analytical narrative

Structure your output as:
## Core Themes
...
## Comparison of Approaches
...
## Research Gaps & Open Problems
...
## Synthesis & Conclusions
...
"""),
    ("human", "Research topic: {topic}\n\nResearch Summary:\n{research_data}"),
])

analyst_chain = analyst_prompt | mistral_llm | StrOutputParser()

# ──────────────────────────────────────────────
# 5. AGENT 3 — Writer (Groq)
#    Converts analysis → formatted Markdown paper
# ──────────────────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an academic research writer. Convert the given analysis into a 
complete, well-structured research paper in Markdown format.

STRICT RULES:
- Output ONLY valid Markdown, nothing else
- Use proper heading hierarchy (# ## ###)
- Include these sections IN ORDER:
  # Title
  ## Abstract
  ## 1. Introduction
  ## 2. Related Work
  ## 3. Methodology
  ## 4. Results & Findings
  ## 5. Discussion
  ## 6. Conclusion
  ## References
- Use **bold** for key terms
- Use bullet points and numbered lists where appropriate
- Format references as: [1] Author, Title, Year
- Write in formal academic tone

Start directly with the # Title — no explanation before or after.
"""),
    ("human", "Topic: {topic}\n\nAnalysis:\n{analysis}"),
])

writer_chain = writer_prompt | groq_llm | StrOutputParser()

# ──────────────────────────────────────────────
# 6. Master Pipeline
# ──────────────────────────────────────────────
def run_research_pipeline(topic: str) -> str:
    # Step 1: Manually call tools, get raw string data
    print(f"\n[bold cyan]🔧 Step 1: Collecting raw data for '{topic}'...[/bold cyan]")
    raw_data = collect_raw_data(topic)
    print("[green]✓ Tools executed[/green]")

    # Step 2: Groq summarizes raw data
    print("\n[bold cyan]🔍 Step 2: Researcher (Groq) summarizing...[/bold cyan]")
    research_summary = researcher_chain.invoke({"topic": topic, "raw_data": raw_data})
    print("[green]✓ Research summary done[/green]")

    # Step 3: Mistral analyses the summary
    print("\n[bold cyan]🧠 Step 3: Analyst (Mistral) analysing...[/bold cyan]")
    analysis = analyst_chain.invoke({"topic": topic, "research_data": research_summary})
    print("[green]✓ Analysis complete[/green]")

    # Step 4: Groq writes Markdown paper
    print("\n[bold cyan]📝 Step 4: Writer (Groq) generating Markdown paper...[/bold cyan]")
    md_output = writer_chain.invoke({"topic": topic, "analysis": analysis})
    print("[green]✓ Markdown generation complete[/green]")

    # Save to .md file
    with open("output_paper.md", "w", encoding="utf-8") as f:
        f.write(md_output)
    print("[bold green]✅ Saved to output_paper.md[/bold green]")

    return md_output