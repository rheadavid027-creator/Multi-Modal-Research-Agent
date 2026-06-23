from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import subprocess
import os
import tempfile
import shutil
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()

# ──────────────────────────────────────────────
# 1. LLMs
# ──────────────────────────────────────────────
groq_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
mistral_llm = ChatMistralAI(model="mistral-medium-latest", temperature=0.3)
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)

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

    try:
        paper_result = scrape_url.invoke({"query": topic})
        results.append(f"## Academic Papers (ArXiv)\n{paper_result}")
    except Exception as e:
        results.append(f"## Academic Papers\nError: {e}")

    # Optional: scrape top URL if web_result has a link
    # try:
    #     scrape_result = scrape_url.invoke({"url": "https://..."})
    #     results.append(f"## Scraped Content\n{scrape_result}")
    # except Exception as e:
    #     pass

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
# 5. AGENT 3 — LaTeX Writer (Gemini)
#    Converts analysis → full LaTeX paper
# ──────────────────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an academic LaTeX writer. Convert the given research analysis into a complete, 
well-structured LaTeX research paper.

STRICT RULES:
- Output ONLY valid LaTeX code, nothing else
- Use \\documentclass{{article}} with packages: geometry, hyperref, amsmath, graphicx, biblatex, booktabs
- Include: Abstract, Introduction, Related Work, Methodology/Discussion, Results/Findings, Conclusion, References
- Use \\section, \\subsection properly
- Format citations as \\cite{{key}} placeholders
- Use itemize/enumerate for lists
- IEEE-style paper format

Start directly with \\documentclass — no explanation before or after.
"""),
    ("human", "Topic: {topic}\n\nAnalysis:\n{analysis}"),
])

writer_chain = writer_prompt | mistral_llm | StrOutputParser()

import subprocess
import os
import tempfile
import shutil

def latex_to_pdf(latex_code: str, output_path: str = "output_paper.pdf") -> str:
    """
    Converts LaTeX string → compiled PDF using pdflatex.
    Returns path to the generated PDF.
    """
    # Clean latex output — Gemini/Mistral kabhi kabhi ```latex fences deta hai
    if "```latex" in latex_code:
        latex_code = latex_code.split("```latex")[1].split("```")[0].strip()
    elif "```" in latex_code:
        latex_code = latex_code.split("```")[1].split("```")[0].strip()

    # Temp directory mein kaam karo (pdflatex ke aux files wahan jayenge)
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, "paper.tex")
        pdf_file = os.path.join(tmpdir, "paper.pdf")

        # .tex file likho
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # pdflatex run karo (2 baar — references/TOC ke liye)
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file],
                cwd=tmpdir,
                capture_output=True,
                text=True,
            )

        if not os.path.exists(pdf_file):
            # Log karo error
            log_file = os.path.join(tmpdir, "paper.log")
            if os.path.exists(log_file):
                with open(log_file, "r") as lf:
                    print(f"[red]LaTeX Error Log:\n{lf.read()[-3000:]}[/red]")
            raise FileNotFoundError("PDF generation failed. Check LaTeX errors above.")

        # PDF ko final output path pe copy karo
        shutil.copy(pdf_file, output_path)
        print(f"[bold green]✅ PDF saved to: {output_path}[/bold green]")
        
        return output_path

# ──────────────────────────────────────────────
# 6. Master Pipeline
# ──────────────────────────────────────────────
def run_research_pipeline(topic: str) -> str:
    print(f"\n[bold cyan]🔧 Step 1: Collecting raw data for '{topic}'...[/bold cyan]")
    raw_data = collect_raw_data(topic)
    print("[green]✓ Tools executed[/green]")

    print("\n[bold cyan]🔍 Step 2: Researcher (Groq) summarizing...[/bold cyan]")
    research_summary = researcher_chain.invoke({"topic": topic, "raw_data": raw_data})
    print("[green]✓ Research summary done[/green]")

    print("\n[bold cyan]🧠 Step 3: Analyst (Mistral) analysing...[/bold cyan]")
    analysis = analyst_chain.invoke({"topic": topic, "research_data": research_summary})
    print("[green]✓ Analysis complete[/green]")

    print("\n[bold cyan]📝 Step 4: Writer generating LaTeX...[/bold cyan]")
    latex_output = writer_chain.invoke({"topic": topic, "analysis": analysis})
    print("[green]✓ LaTeX generation complete[/green]")

    # Save .tex file
    with open("output_paper.tex", "w", encoding="utf-8") as f:
        f.write(latex_output)
    print("[green]✓ .tex file saved[/green]")

    # ── NEW: Compile to PDF ──
    print("\n[bold cyan]🖨️  Step 5: Compiling LaTeX → PDF...[/bold cyan]")
    pdf_path = latex_to_pdf(latex_output, output_path="output_paper.pdf")

    return pdf_path




# ──────────────────────────────────────────────
# 7. Run & Save
# ──────────────────────────────────────────────
