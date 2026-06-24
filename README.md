# Multi-Modal Research Agent

A cutting-edge AI-powered research paper generator that uses a **multi-agent pipeline** to automatically research, analyze, and synthesize research papers on any topic. This application leverages multiple Large Language Models (LLMs) and web tools to create comprehensive, well-structured academic papers in Markdown format.

![Multi-Modal Research Agent](https://img.shields.io/badge/AI-Research%20Automation-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)

---

## 🎯 Overview

The Multi-Modal Research Agent is designed to automate the research paper generation process by:
- **Collecting** real-time data from the web using advanced search tools
- **Summarizing** findings through a research agent
- **Analyzing** data from multiple perspectives using a critical analyst
- **Writing** polished academic papers formatted in Markdown

Instead of spending hours researching and writing, you simply enter a topic and let the AI handle the heavy lifting.

---

## 🏗️ Architecture

The application uses a **three-stage multi-agent pipeline** powered by different LLMs:

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT (Research Topic)                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: DATA COLLECTION (Tools + Raw Processing)               │
├─────────────────────────────────────────────────────────────────┤
│ • Web Search Tool (Tavily API) → Fetch recent, reliable sources │
│ • Web Scraping Tool (BeautifulSoup) → Extract full content      │
│ Output: Raw markdown-formatted data from web sources            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: RESEARCHER AGENT (Groq / LLaMA-3.3-70B)                │
├─────────────────────────────────────────────────────────────────┤
│ • Processes raw web data                                        │
│ • Extracts key facts, findings, and methodologies               │
│ • Organizes information into structured sections:               │
│   - Web Findings                                                │
│   - Academic Papers                                             │
│   - Key Facts & Data Points                                     │
│ Output: Clean, structured research summary                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: ANALYST AGENT (Mistral AI / Mistral-Medium)            │
├─────────────────────────────────────────────────────────────────┤
│ • Deep analysis of researcher summary                           │
│ • Identifies core themes and arguments                          │
│ • Compares different sources and approaches                     │
│ • Spots gaps and contradictions                                 │
│ • Synthesizes conclusions                                       │
│ Output: Critical analysis and comprehensive insights            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: WRITER AGENT (Groq / LLaMA-3.3-70B)                    │
├─────────────────────────────────────────────────────────────────┤
│ • Converts analysis into academic format                        │
│ • Generates complete research paper with:                       │
│   - Title                                                       │
│   - Abstract                                                    │
│   - Introduction                                                │
│   - Related Work                                                │
│   - Methodology                                                 │
│   - Results & Findings                                          │
│   - Discussion                                                  │
│   - Conclusion                                                  │
│   - References                                                  │
│ Output: Polished Markdown research paper                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│            STREAMLIT UI - PREVIEW & DOWNLOAD                    │
├─────────────────────────────────────────────────────────────────┤
│ • Display paper in real-time                                    │
│ • Download as .md file                                          │
│ • Save copy locally as backup                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Key Components

### 1. **Tools Module** (`tools.py`)
Contains LangChain-based tools for data collection:

| Tool | Purpose | Source |
|------|---------|--------|
| `web_search()` | Search for recent, reliable information | Tavily API |
| `scrape_url()` | Extract clean text from webpages | BeautifulSoup + Requests |

### 2. **Agent Module** (`agent.py`)
Core pipeline orchestration with three specialized agents:

**Agent 1: Researcher (Groq LLaMA-3.3)**
- Summarizes raw web data
- Structures findings into organized sections
- Cleans and formats information

**Agent 2: Analyst (Mistral AI)**
- Performs deep analysis on research summary
- Identifies themes, contradictions, and gaps
- Synthesizes findings into coherent narrative

**Agent 3: Writer (Groq LLaMA-3.3)**
- Transforms analysis into academic format
- Ensures proper Markdown structure
- Adds titles, sections, and formatting
- Generates references

### 3. **CLI Interface** (`app.py`)
Command-line version for batch processing:
- Takes topic as input
- Runs full pipeline
- Outputs LaTeX formatted paper

### 4. **Streamlit Web UI** (`streamlit_app.py`)
Interactive web interface featuring:
- Beautiful, modern UI with custom styling
- Real-time processing feedback
- Paper preview in Markdown
- One-click download functionality
- Session state management

---

## 🚀 How It Works (Detailed Flow)

### Step 1: Data Collection
```
User Input: "Machine Learning in Healthcare"
           ↓
    Web Search Tool
           ↓
Tavily API returns 5 best sources with titles and URLs
           ↓
    Web Scraping Tool
           ↓
BeautifulSoup extracts main content from first URL (first 3000 chars)
           ↓
Raw data compiled into markdown-formatted string
```

### Step 2: Research Summarization
```
Raw Data (2000+ chars)
           ↓
Researcher Agent (LLaMA-3.3)
    ↓ Prompt asks to:
      - Extract key facts
      - Organize findings
      - Identify methodologies
           ↓
Structured Summary (~500-800 words)
    - Web Findings
    - Academic Papers
    - Key Facts & Data Points
```

### Step 3: Critical Analysis
```
Research Summary
           ↓
Analyst Agent (Mistral)
    ↓ Prompt asks to:
      - Find core themes
      - Compare approaches
      - Identify gaps
      - Synthesize conclusions
           ↓
Deep Analysis (~800-1200 words)
    - Core Themes
    - Comparison of Approaches
    - Research Gaps & Open Problems
    - Synthesis & Conclusions
```

### Step 4: Academic Writing
```
Deep Analysis
           ↓
Writer Agent (LLaMA-3.3)
    ↓ Prompt asks to:
      - Format as academic paper
      - Use proper Markdown
      - Add all required sections
      - Include references
           ↓
Complete Research Paper (~2000-3000 words)
    With sections:
    # Title
    ## Abstract
    ## 1. Introduction
    ## 2. Related Work
    ## 3. Methodology
    ## 4. Results & Findings
    ## 5. Discussion
    ## 6. Conclusion
    ## References
```

---

## 💻 Technology Stack

### Core Framework
- **Python 3.8+** - Programming language
- **LangChain** - LLM orchestration and chain management
- **Streamlit** - Web UI framework

### Language Models (Multi-Modal)
- **Groq LLaMA-3.3-70B** - Data collection & writing (fast inference)
- **Mistral AI (Mistral-Medium)** - Analysis & deep reasoning

### Data Collection
- **Tavily Search API** - Web search results
- **BeautifulSoup 4** - Web scraping
- **Requests** - HTTP client

### Utilities
- **python-dotenv** - Environment variable management
- **Rich** - Beautiful terminal output
- **Pydantic** - Data validation
- **Tiktoken** - Token counting
- **Tenacity** - Retry logic
- **Pandas** - Data handling (optional)

---

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- API keys for:
  - Tavily Search API
  - Groq (free tier available)
  - Mistral AI
  - (Optional) OpenAI, Google Generative AI

### Step 1: Clone Repository
```bash
cd c:\AI\Multi-model-Reserach-agent\Multi-Modal-Research-Agent
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Set Up Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENAI_API_KEY=your_openai_api_key (optional)
GOOGLE_API_KEY=your_google_api_key (optional)
```

**Alternative (for Streamlit):** Create `.streamlit/secrets.toml`
```toml
GROQ_API_KEY = "your_groq_api_key"
MISTRAL_API_KEY = "your_mistral_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
```

### Step 6: Run the Application

**Option A: Streamlit Web UI (Recommended)**
```bash
streamlit run streamlit_app.py
```
Opens at: `http://localhost:8501`

**Option B: Command-Line Interface**
```bash
python app.py
```
Prompts for topic, outputs `<topic_name>.tex`

---

## 🎮 How to Use

### Using Streamlit Web UI

1. **Launch the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Enter a research topic** in the text input:
   - Example: "Applications of Machine Learning in Healthcare"
   - Example: "Quantum Computing and Cryptography"
   - Example: "Climate Change Mitigation Strategies"

3. **Click "Run Research Pipeline"**
   - Watch real-time progress updates
   - Each stage completes with visual confirmation

4. **Review the Generated Paper**
   - Paper appears in preview below
   - Markdown-formatted and ready to read
   - Includes all academic sections

5. **Download the Paper**
   - Click "Download Markdown Research Paper"
   - File saves as `topic_topic_topic.md`
   - Open in any text editor or Markdown viewer

### Using CLI Interface

1. **Run the script:**
   ```bash
   python app.py
   ```

2. **Enter your topic when prompted**

3. **Wait for completion**

4. **Find output file:**
   - Saved as `<first_4_words_of_topic>.tex`
   - Preview printed to terminal (first 500 chars)

---

## 📁 Output Files

### Generated Papers
- **`output_paper.md`** - Last generated paper in Markdown
- **`[topic]_[topic].md`** - Downloaded paper (Streamlit saves with topic name)
- **`[topic].tex`** - LaTeX formatted paper (CLI only)

### Example Output Structure
```markdown
# Machine Learning Applications in Healthcare

## Abstract
This paper explores the transformative role of machine learning...

## 1. Introduction
Machine learning has emerged as a critical technology...

## 2. Related Work
Previous research in this domain has focused on...

## 3. Methodology
Our analysis framework integrates...

## 4. Results & Findings
Key findings include:
- Finding 1: ...
- Finding 2: ...

## 5. Discussion
The implications of these findings suggest...

## 6. Conclusion
In conclusion, machine learning represents...

## References
[1] Author et al., Title, Year
[2] ...
```

---

## 🔌 API Requirements & Pricing

| Service | Purpose | Pricing | Sign-Up |
|---------|---------|---------|---------|
| **Groq** | LLaMA-3.3 LLM | Free tier available | https://console.groq.com |
| **Mistral AI** | Analysis model | Free tier + paid | https://console.mistral.ai |
| **Tavily** | Web Search | Free tier (5 searches/day) | https://tavily.com |

**Estimated Cost per Paper:** $0.01-0.10 USD (varies with model usage)

---

## ⚙️ Configuration & Customization

### Modify LLM Models
Edit `agent.py`:
```python
groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Change model here
    temperature=0.2                    # Adjust creativity (0-1)
)

mistral_llm = ChatMistralAI(
    model="mistral-medium-latest",    # Change model here
    temperature=0.3                    # Adjust creativity (0-1)
)
```

### Adjust Temperature (Creativity)
- **0.0** - Deterministic, focused answers
- **0.5** - Balanced
- **1.0** - Creative, varied responses

### Modify Paper Sections
Edit the `writer_prompt` in `agent.py` to change paper structure:
```python
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """... 
    - Include these sections IN ORDER:
      # Title
      ## Abstract
      # YOUR NEW SECTION HERE
      ...
    """),
```

### Change UI Styling
Edit `streamlit_app.py` CSS in `PAGE_STYLE` variable:
```python
PAGE_STYLE = """
<style>
    body { background-color: #YOUR_COLOR; }
    ...
</style>
"""
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **API Key Errors** | Check `.env` file, ensure keys are valid and have permissions |
| **Streamlit Not Starting** | Run `pip install streamlit` or check port 8501 availability |
| **Web Scraping Fails** | Some sites block scrapers; Tavily API may need configuration |
| **Timeout Errors** | Increase timeout in `tools.py` scrape_url() function |
| **Poor Paper Quality** | Try adjusting temperature values for different models |
| **Memory Issues** | Reduce `max_results` in Tavily search or limit scrape size |

---

## 📊 Performance Metrics

| Metric | Expected Value |
|--------|-----------------|
| Data Collection | 5-15 seconds |
| Researcher Agent | 10-20 seconds |
| Analyst Agent | 15-30 seconds |
| Writer Agent | 10-20 seconds |
| **Total Time** | **40-85 seconds** |
| Output Length | 2,000-3,500 words |
| Cost per Paper | ~$0.01-0.10 |

---

## 🎯 Use Cases

1. **Academic Research** - Quick literature reviews and synthesis
2. **Content Creation** - Generate blog posts on any topic
3. **Learning** - Understand complex topics through AI-generated papers
4. **Business Research** - Market analysis and competitive intelligence
5. **Journalism** - Quick research briefs on trending topics
6. **Education** - Teaching material generation
7. **Knowledge Consolidation** - Compile scattered research into coherent papers

---

## 🔒 Security & Privacy

- **API Keys** - Stored in `.env` files (never commit to git)
- **Web Scraping** - Respects robots.txt and rate limits
- **Data Retention** - Local files only, no cloud storage
- **User Privacy** - No data tracking or analytics

### Best Practices
1. Never share `.env` files
2. Add `.env` to `.gitignore`:
   ```
   .env
   .streamlit/secrets.toml
   *.md
   *.tex
   venv/
   ```
3. Rotate API keys regularly
4. Use separate API keys for production

---

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] PDF export format
- [ ] Citation management (BibTeX, APA, MLA)
- [ ] Real-time editing of papers
- [ ] Paper comparison tools
- [ ] Custom prompts for specialized domains
- [ ] Batch processing for multiple topics
- [ ] Paper quality scoring
- [ ] Fact-checking integration
- [ ] Image and diagram generation

---

## 📝 License

This project is provided as-is for educational and research purposes.

---

## 💡 Tips & Tricks

### For Better Results
- **Be specific** with your topic: "Quantum Computing" vs "Recent breakthroughs in quantum error correction for NISQ devices"
- **Use recent topics** for best web search results
- **Review output** and refine topics for specialized areas
- **Combine outputs** from multiple topic searches for comprehensive papers

### Advanced Usage
```python
# Programmatic usage in other scripts
from agent import run_research_pipeline

topic = "Your research topic"
paper = run_research_pipeline(topic)
print(paper)
```

### Batch Processing
```bash
# Create a script to process multiple topics
for topic in "Topic1" "Topic2" "Topic3"; do
    python app.py <<< "$topic"
done
```

---

## 📧 Support & Contact

For issues, questions, or improvements, please refer to the code documentation and comments in each module.

---

**Made with ❤️ using LangChain, Streamlit, and AI**

---

## 🌟 Features at a Glance

✅ **Multi-Agent Architecture** - Specialized agents for different tasks  
✅ **Real-time Web Research** - Pulls current information via Tavily API  
✅ **Advanced NLP** - Uses state-of-the-art LLMs (LLaMA-3, Mistral)  
✅ **Beautiful Web UI** - Streamlit interface with modern design  
✅ **Markdown Output** - Academic-format papers  
✅ **Fast Processing** - Complete paper in under 2 minutes  
✅ **Scalable** - Works with any research topic  
✅ **Customizable** - Modify models, prompts, and behavior  
✅ **CLI & Web Options** - Flexible usage modes  
✅ **Well-Documented** - Detailed code comments and logs  
