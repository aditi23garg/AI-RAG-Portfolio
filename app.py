import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import requests

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------
load_dotenv()

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Search Aditi",
    
    page_icon="⚡",
    layout="centered"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    .stApp {
        background-color: #09090b;
        color: #f4f4f5;
        font-family: 'DM Mono', monospace;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 40px !important;
        max-width: 780px !important;
    }

    /* ---- HERO ---- */
    .hero-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 52vh;
        padding-top: 80px;
        padding-bottom: 20px;
        position: relative;
    }
    .glow-ring {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -55%);
        width: 340px; height: 340px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(124,58,237,0.18) 0%, transparent 70%);
        pointer-events: none;
        animation: pulse-ring 3s ease-in-out infinite;
    }
    @keyframes pulse-ring {
        0%, 100% { opacity: 0.6; transform: translate(-50%, -55%) scale(1); }
        50%       { opacity: 1;   transform: translate(-50%, -55%) scale(1.08); }
    }
    .wordmark {
        font-family: 'Syne', sans-serif;
        font-size: 15px; font-weight: 600;
        letter-spacing: 0.35em; text-transform: uppercase;
        color: #7c3aed; margin-bottom: 22px;
        position: relative; z-index: 2;
    }
    .logo-text {
        font-family: 'Syne', sans-serif;
        font-size: clamp(52px, 9vw, 86px);
        font-weight: 800; line-height: 0.95;
        text-align: center; letter-spacing: -0.03em;
        position: relative; z-index: 2;
        background: linear-gradient(135deg, #f4f4f5 30%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 18px;
    }
    .tagline {
        font-family: 'DM Mono', monospace;
        font-size: 13px; color: #71717a;
        letter-spacing: 0.04em; text-align: center;
        position: relative; z-index: 2;
        margin-bottom: 20px;
    }

    /* ---- SOCIAL BADGES ---- */
    .badges-row {
        display: flex; gap: 10px;
        justify-content: center; flex-wrap: wrap;
        margin-bottom: 10px; position: relative; z-index: 2;
    }
    .badge-link {
        display: inline-flex; align-items: center; gap: 7px;
        background: #18181b; border: 1.5px solid #3f3f46;
        border-radius: 50px; padding: 7px 16px;
        font-family: 'DM Mono', monospace; font-size: 12px;
        color: #a1a1aa; text-decoration: none;
        transition: all 0.2s;
    }
    .badge-link:hover { color: #f4f4f5; border-color: #7c3aed; background: rgba(124,58,237,0.08); }
    .badge-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
    .dot-linkedin { background: #0a66c2; }
    .dot-github   { background: #f4f4f5; }
    .dot-codechef { background: #f5a623; }

    /* ---- SEARCH BOX ---- */
    .stTextInput > div > div > input {
        background: #18181b !important;
        border: 1.5px solid #3f3f46 !important;
        border-radius: 14px !important;
        color: #f4f4f5 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 16px !important;
        padding: 18px 22px !important;
        height: auto !important;
        box-shadow: 0 0 0 0 transparent !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #52525b !important; }
    .stTextInput label { display: none !important; }

    /* ---- CHIPS ---- */
    .chips-label {
        font-family: 'DM Mono', monospace;
        font-size: 11px; letter-spacing: 0.12em;
        text-transform: uppercase; color: #52525b;
        text-align: center; margin-bottom: 12px; margin-top: 20px;
    }
    div[data-testid="column"] .stButton > button {
        background: transparent !important;
        border: 1.5px solid #3f3f46 !important;
        border-radius: 50px !important;
        color: #a1a1aa !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 12px !important;
        padding: 7px 14px !important;
        cursor: pointer !important;
        transition: all 0.18s !important;
        white-space: nowrap !important;
        width: 100% !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        border-color: #7c3aed !important;
        color: #a78bfa !important;
        background: rgba(124,58,237,0.08) !important;
    }

    /* ---- DIVIDER ---- */
    .section-divider { border: none; border-top: 1px solid #27272a; margin: 36px 0; }

    /* ---- RESULT META ---- */
    .result-meta {
        font-family: 'DM Mono', monospace;
        font-size: 11px; color: #52525b;
        letter-spacing: 0.08em; text-transform: uppercase;
        margin-bottom: 14px;
        display: flex; align-items: center; gap: 10px;
    }
    .result-meta::before {
        content: ''; display: inline-block;
        width: 6px; height: 6px;
        background: #7c3aed; border-radius: 50%;
    }

    /* ---- RESULT CARD ---- */
    .result-card {
        background: #18181b; border: 1px solid #27272a;
        border-radius: 16px; padding: 28px 30px;
        line-height: 1.8; font-size: 15px; color: #d4d4d8;
        font-family: 'DM Mono', monospace;
        position: relative; overflow: hidden;
    }
    .result-card::before {
        content: ''; position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #7c3aed, #a78bfa, transparent);
    }
    .result-card strong { color: #f4f4f5; font-weight: 500; }

    /* ---- MARKDOWN INSIDE RESULT CARD ---- */
    /* target Streamlit markdown blocks that follow the card opening div */
    .result-card + div p,
    .result-card + div li,
    .result-card + div h3,
    .result-card + div h4,
    .result-card + div code {
        font-family: 'DM Mono', monospace !important;
    }
    /* Style markdown rendered via st.markdown after the card div */
    [data-testid="stMarkdownContainer"] h3 {
        font-family: 'Syne', sans-serif !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #a78bfa !important;
        margin-top: 18px !important;
        margin-bottom: 6px !important;
        letter-spacing: 0.02em;
    }
    [data-testid="stMarkdownContainer"] h4 {
        font-family: 'Syne', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #7c3aed !important;
        margin-top: 14px !important;
        margin-bottom: 4px !important;
    }
    [data-testid="stMarkdownContainer"] p {
        font-family: 'DM Mono', monospace !important;
        font-size: 14px !important;
        color: #d4d4d8 !important;
        line-height: 1.8 !important;
        margin-bottom: 8px !important;
    }
    [data-testid="stMarkdownContainer"] li {
        font-family: 'DM Mono', monospace !important;
        font-size: 14px !important;
        color: #d4d4d8 !important;
        line-height: 1.8 !important;
        margin-bottom: 4px !important;
    }
    [data-testid="stMarkdownContainer"] strong {
        color: #f4f4f5 !important;
        font-weight: 600 !important;
    }
    [data-testid="stMarkdownContainer"] ul {
        padding-left: 20px !important;
        margin-bottom: 10px !important;
    }
    [data-testid="stMarkdownContainer"] a {
        color: #a78bfa !important;
        text-decoration: none !important;
    }
    [data-testid="stMarkdownContainer"] a:hover {
        color: #f4f4f5 !important;
        text-decoration: underline !important;
    }
    [data-testid="stMarkdownContainer"] code {
        background: #09090b !important;
        border: 1px solid #3f3f46 !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
        font-size: 12px !important;
        color: #a78bfa !important;
    }

    /* ---- GITHUB PANEL ---- */
    .gh-panel {
        background: #18181b; border: 1px solid #27272a;
        border-radius: 16px; padding: 20px 24px;
        margin-top: 14px;
    }
    .gh-panel-title {
        font-family: 'DM Mono', monospace;
        font-size: 11px; letter-spacing: 0.1em;
        text-transform: uppercase; color: #52525b;
        margin-bottom: 14px;
    }
    .gh-repo-card {
        background: #09090b; border: 1px solid #27272a;
        border-radius: 10px; padding: 12px 16px;
        margin-bottom: 10px;
    }
    .gh-repo-name {
        font-family: 'Syne', sans-serif;
        font-size: 14px; font-weight: 600; color: #a78bfa;
        text-decoration: none;
    }
    .gh-repo-desc { font-size: 12px; color: #71717a; margin-top: 4px; line-height: 1.5; }
    .gh-repo-meta { display: flex; gap: 14px; margin-top: 8px; }
    .gh-meta-item { font-size: 11px; color: #52525b; }
    .gh-stats-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 14px; }
    .gh-stat-pill {
        background: #09090b; border: 1px solid #27272a;
        border-radius: 50px; padding: 6px 14px;
        font-size: 12px; color: #a1a1aa;
        font-family: 'DM Mono', monospace;
    }
    .gh-stat-pill span { color: #f4f4f5; font-weight: 600; }

    /* ---- SPINNER ---- */
    .stSpinner > div { border-top-color: #7c3aed !important; }

    /* ---- FOOTER ---- */
    .footer {
        text-align: center; font-family: 'DM Mono', monospace;
        font-size: 11px; color: #3f3f46;
        letter-spacing: 0.06em; margin-top: 60px; padding-bottom: 20px;
    }
    .footer span { color: #52525b; }

    .element-container { margin-bottom: 0 !important; }

    /* ---- DOWNLOAD RESUME BUTTON ---- */
    div[data-testid="stDownloadButton"] > button {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background: transparent !important;
        border: 1.5px solid #7c3aed !important;
        border-radius: 50px !important;
        color: #a78bfa !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 13px !important;
        padding: 10px 24px !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        margin: 0 auto !important;
        width: auto !important;
        letter-spacing: 0.04em !important;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: rgba(124,58,237,0.12) !important;
        color: #f4f4f5 !important;
        border-color: #a78bfa !important;
        transform: translateY(-1px) !important;
    }
    div[data-testid="stDownloadButton"] > button:active {
        transform: translateY(0px) !important;
    }
    .download-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 18px;
        margin-bottom: 4px;
    }
    .download-hint {
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        color: #3f3f46;
        text-align: center;
        letter-spacing: 0.06em;
        margin-top: 6px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# GITHUB DATA FETCHER
# -----------------------------------
GITHUB_USERNAME = "aditi23garg"
CODECHEF_USERNAME = "aditi_garg23"

@st.cache_data(ttl=3600)   # cache for 1 hour
def fetch_github_data():
    """Fetch repos and profile from GitHub public API. No token needed for public data."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")  # optional — raises rate limit from 60 to 5000 req/hr
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # Profile
        profile_resp = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}",
            headers=headers, timeout=8
        )
        profile = profile_resp.json() if profile_resp.status_code == 200 else {}

        # Repos
        repos_resp = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=50&sort=updated",
            headers=headers, timeout=8
        )
        repos = repos_resp.json() if repos_resp.status_code == 200 else []
        if not isinstance(repos, list):
            repos = []

        # Sort by stars then updated
        repos_sorted = sorted(repos, key=lambda r: (r.get("stargazers_count", 0), r.get("updated_at", "")), reverse=True)

        # Language tally
        lang_count = {}
        for r in repos:
            lang = r.get("language")
            if lang:
                lang_count[lang] = lang_count.get(lang, 0) + 1

        return {
            "profile": profile,
            "repos": repos_sorted[:6],          # top 6 for display
            "all_repos": repos,
            "total_repos": profile.get("public_repos", len(repos)),
            "followers": profile.get("followers", 0),
            "following": profile.get("following", 0),
            "languages": lang_count,
            "total_stars": sum(r.get("stargazers_count", 0) for r in repos),
        }
    except Exception:
        return {"profile": {}, "repos": [], "all_repos": [], "total_repos": 35,
                "followers": 0, "following": 0, "languages": {}, "total_stars": 0}


def build_github_context(gh_data):
    """Convert GitHub data into a text block for the RAG context."""
    repos = gh_data.get("all_repos", [])
    langs = gh_data.get("languages", {})
    total  = gh_data.get("total_repos", 0)
    stars  = gh_data.get("total_stars", 0)

    lines = [
        f"GitHub Profile: https://github.com/{GITHUB_USERNAME}",
        f"Total public repositories: {total}",
        f"Total stars received: {stars}",
        f"GitHub followers: {gh_data.get('followers', 0)}",
        "",
        "Top programming languages used on GitHub:",
    ]
    for lang, count in sorted(langs.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  - {lang}: {count} repositories")

    lines += ["", "GitHub Repositories (sample):"]
    for r in repos[:15]:
        name  = r.get("name", "")
        desc  = r.get("description") or "No description"
        lang  = r.get("language") or "N/A"
        stars = r.get("stargazers_count", 0)
        url   = r.get("html_url", "")
        lines.append(f"  - {name} ({lang}, ⭐{stars}): {desc} | {url}")

    return "\n".join(lines)


CODECHEF_CONTEXT = """
CodeChef Profile: https://www.codechef.com/users/aditi_garg23
Username: aditi_garg23
Institution: Indian Institute of Technology Gandhinagar, Gujarat, India
League: Gold League
Country: India
Status: Student

Total Problems Solved: 1190
Problem Solver Badge: Diamond (awarded for solving 1000+ problems)
Daily Streak Badge: Silver (maintained a 25-day streak)

Completed Learning Paths on CodeChef:
  - Learn SQL (Completed)
  - Learn NumPy - Practice Problems and Challenges (Completed)
  - Learn Pandas - Practice Problems and Challenges (Completed)
  - Problem Solving in Python (Completed) — Certificate issued March 2026
  - Learn Python Programming (Completed)
  - Git/GitHub (Completed)
  - Learn Advanced SQL (91% progress)

Practice Paths in progress:
  - 500 to 1000 difficulty problems (74%)
  - Practice Strings (9%)
  - Python Coding Challenges (10%)
  - Stacks and Queues (13%)
  - Practice Arrays (7%)
  - Practice Sorting (7%)

Skill Tests:
  - Python Skill Test: 97% score (attempted March 2026)

Certificates:
  - Problem Solving in Python — issued March 2026
    URL: https://www.codechef.com/certificates/public/ca1c660
"""

# -----------------------------------
# LOAD PDF TEXT
# -----------------------------------
def load_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

resume_text  = load_pdf_text("data/resume.pdf")
project_text = load_pdf_text("data/projects.pdf")

# -----------------------------------
# RAG RETRIEVAL
# -----------------------------------
def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def retrieve_relevant_chunks(query, chunks, top_k=4):
    query_words = query.lower().split()
    scored = [(sum(1 for w in query_words if w in c.lower()), c) for c in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return "\n".join([c for _, c in scored[:top_k]])

# -----------------------------------
# GROQ CLIENT
# -----------------------------------
client    = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# -----------------------------------
# FETCH GITHUB LIVE
# -----------------------------------
gh_data        = fetch_github_data()
github_context = build_github_context(gh_data)

# Build all chunks (PDF + GitHub + CodeChef)
all_text   = resume_text + "\n" + project_text + "\n" + github_context + "\n" + CODECHEF_CONTEXT
all_chunks = chunk_text(all_text)

# -----------------------------------
# HERO
# -----------------------------------
st.markdown(
    """
    <div class='hero-wrapper'>
        <div class='glow-ring'></div>
        <div class='wordmark'>AI Portfolio Search</div>
        <div class='logo-text'>Search<br/>Aditi.</div>
        <div class='tagline'>// resume · github · codechef · all in one search</div>
        <div class='badges-row'>
            <a class='badge-link' href='https://www.linkedin.com/in/aditigarg23199' target='_blank'>
                <span class='badge-dot dot-linkedin'></span> LinkedIn
            </a>
            <a class='badge-link' href='https://github.com/aditi23garg' target='_blank'>
                <span class='badge-dot dot-github'></span> GitHub
            </a>
            <a class='badge-link' href='https://www.codechef.com/users/aditi_garg23' target='_blank'>
                <span class='badge-dot dot-codechef'></span> CodeChef
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# RESUME DOWNLOAD BUTTON
# -----------------------------------
try:
    with open("data/resume.pdf", "rb") as pdf_file:
        resume_bytes = pdf_file.read()

    st.markdown("<div class='download-wrapper'>", unsafe_allow_html=True)
    st.download_button(
        label="⬇  Download Resume",
        data=resume_bytes,
        file_name="Aditi_Garg_Resume.pdf",
        mime="application/pdf",
        key="resume_download"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='download-hint'>PDF · for hiring managers</div>",
        unsafe_allow_html=True
    )
except FileNotFoundError:
    pass   # silently skip if PDF not found in path

# -----------------------------------
# SEARCH INPUT
# -----------------------------------
query = st.text_input(
    "",
    placeholder="Ask anything — projects, skills, GitHub repos, CodeChef rating...",
    key="main_search"
)

# -----------------------------------
# QUICK CHIPS — 6 chips, 2 rows of 3
# -----------------------------------
st.markdown("<div class='chips-label'>Quick searches</div>", unsafe_allow_html=True)

quick_questions = [
    "🛠  Tech Stack",
    "💼  Work Experience",
    "🚀  Projects",
    "🐙  GitHub Repos",
    "🏆  CodeChef Stats",
    "📜  Certifications",
]

chip_cols     = st.columns(3)
selected_chip = None

for i, label in enumerate(quick_questions):
    with chip_cols[i % 3]:
        if st.button(label, key=f"chip_{i}"):
            selected_chip = label.split("  ")[1]

final_query = selected_chip if selected_chip else query

# -----------------------------------
# RESPONSE
# -----------------------------------
if final_query:
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='result-meta'>Result for &nbsp;'{final_query}'</div>",
        unsafe_allow_html=True
    )

    relevant_context = retrieve_relevant_chunks(final_query, all_chunks)

    # Detect query type to switch system prompt
    project_keywords = [
        "project", "projects", "built", "build", "developed", "application",
        "app", "system", "model", "prediction", "agent", "voice", "ncert",
        "admitguard", "loan", "delivery", "delay", "study assistant"
    ]
    is_project_query = any(kw in final_query.lower() for kw in project_keywords)

    if is_project_query:
        system_prompt = f"""You are a senior AI/ML technical writer presenting Aditi Garg's projects to hiring managers, CTOs and engineering teams.

Your task: produce a DEEP, DETAILED, technically rich breakdown of every project mentioned in the context.

════════════════════════════════════════
OUTPUT FORMAT — use this structure for EACH project:
════════════════════════════════════════

---
### 🚀 [Project Name]

**Overview**
2-3 sentences: the real-world problem, who faces it, and what this project delivers as a solution.

**Problem Statement**
Why does this problem exist? What are the consequences of not solving it? (1-2 sentences of industry context)

**How It Works — Architecture & Pipeline**
Walk through the end-to-end technical flow as numbered steps, e.g.:
1. Data Collection / Input
2. Preprocessing & Feature Engineering
3. Model / AI Core
4. Output / Interface / Deployment

For each step, explain WHAT happens and WHY that approach was chosen over alternatives.

**Tech Stack Breakdown**
| Tool / Library | Role in this project |
|---|---|
| Python | Core language for data processing and model logic |
| ... | ... |
(fill with actual tools from context, add explanation column)

**Key Technical Decisions**
- Why this ML algorithm / architecture was the right choice for this problem
- Any interesting engineering tradeoffs made
- How accuracy, latency, or scale was addressed

**Results & Impact**
- Quantified metrics if available (accuracy, F1, latency, dataset size)
- Real-world applicability — who would deploy this and why
- What it demonstrates about Aditi's skill level

**Recruiter Takeaway**
One bold sentence summarising what this project proves about Aditi as an engineer.

---

════════════════════════════════════════
ENRICHMENT RULES — CRITICAL, read carefully:
════════════════════════════════════════

Use the document context as your FOUNDATION. Then apply your deep technical knowledge to ENRICH each point:

PROJECT-SPECIFIC ENRICHMENT GUIDANCE:

1. **Delivery Delay Prediction**
   - Enrich with: supply chain ML context, feature engineering on logistics data (carrier, distance, weather, historical delays), classification vs regression choice, importance of precision/recall in business cost context, how such models are used in e-commerce operations teams.

2. **Voice AI Agent**
   - Enrich with: full STT → LLM → TTS pipeline architecture, latency challenges in real-time voice, how intent detection works, tool-calling / function-calling patterns in LLM agents, WebSocket vs REST for streaming audio, use cases in customer service automation.

3. **NCERT Science Study Assistant (LLM / RAG)**
   - Enrich with: RAG pipeline internals (document chunking strategies, embedding models, vector similarity search, context window management), why RAG outperforms pure fine-tuning for domain Q&A, LangChain components used (document loaders, text splitters, retrievers, chains), educational AI use cases.

4. **AdmitGuard**
   - Enrich with: rule-based vs ML validation systems, how compliance engines work in admissions, data integrity checks, audit logging patterns, exception handling in business rule engines, how AI Studio was used for code generation.

5. **Loan Default Prediction**
   - Enrich with: credit risk modelling context, class imbalance handling (SMOTE, class weights), key financial features (credit score, DTI ratio, payment history), model interpretability with SHAP/feature importance for regulatory compliance, how banks use such models in underwriting.

GENERAL ENRICHMENT:
- For any ML model mentioned: explain why it fits the problem (bias-variance, data size, interpretability needs)
- For any API/framework: explain its specific role and what it enables technically
- For any data pipeline: describe the ingestion → cleaning → feature → model → serving flow
- Add real-world industry context for why the problem matters commercially

HARD RULES:
- NEVER invent project facts, numbers or technologies not implied by the context
- If a specific metric isn't in the context, say "exact metrics not documented" — don't fabricate numbers
- Keep tone confident, third-person, technically precise
- Format the table using markdown pipe syntax

--- CONTEXT START ---
{relevant_context}
--- CONTEXT END ---"""
    else:
        system_prompt = f"""You are an intelligent portfolio assistant for Aditi Garg, an AI/ML Engineer.
Your job is to give hiring managers, recruiters and collaborators rich, well-structured answers about her background.

You have access to three data sources:
1. Resume and project documents (PDFs)
2. Live GitHub profile (repos, languages, stars)
3. CodeChef profile (problems solved, badges, certifications, learning paths)

FORMATTING RULES — always follow these:
- Use **bold** for names, titles, tools, companies and important terms.
- Use `### Section Header` to group related information when the answer has multiple parts.
- Use bullet points (`-`) for lists of items.
- For certifications: show name, issuer and date on separate lines with a bullet each.
- For experience: show role + company + dates as a header, then responsibilities as bullets.
- For skills/tech stack: group by category (Languages, Frameworks, Cloud, etc.) with sub-bullets.
- For CodeChef: always mention total problems solved, badge level, skill test score, and list certificates with dates.
- For GitHub: mention total repos, top languages, and highlight notable repositories with descriptions.
- End every answer with a short one-line summary or takeaway about Aditi.
- Keep a professional, confident, third-person tone — like a recruiter presenting a strong candidate.

STRICT DATA RULES:
- Answer ONLY using information present in the context below. Do NOT invent anything.
- If asked about contact or profiles, always include:
    - LinkedIn: https://www.linkedin.com/in/aditigarg23199
    - GitHub: https://github.com/aditi23garg
    - CodeChef: https://www.codechef.com/users/aditi_garg23
- If something is not in the context, say: "This detail is not mentioned in the available documents."

--- CONTEXT START ---
{relevant_context}
--- CONTEXT END ---"""

    with st.spinner("Searching across resume, GitHub & CodeChef…"):
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": final_query}
            ],
            temperature=0.3,
            max_tokens=2500   # more room for detailed project explanations
        )

    answer = response.choices[0].message.content

    # Render inside styled card wrapper using st.markdown for proper markdown support
    st.markdown(
        "<div class='result-card'>",
        unsafe_allow_html=True
    )
    st.markdown(answer)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---- Show GitHub panel when query is GitHub-related ----
    github_keywords = ["github", "repo", "repositories", "code", "project", "open source", "starred", "language"]
    if any(kw in final_query.lower() for kw in github_keywords) and gh_data.get("repos"):
        repos = gh_data["repos"]
        langs = gh_data["languages"]
        total_stars = gh_data["total_stars"]
        total_repos = gh_data["total_repos"]

        lang_pills = " ".join(
            f"<span class='gh-stat-pill'>{lang} <span>{cnt}</span></span>"
            for lang, cnt in sorted(langs.items(), key=lambda x: x[1], reverse=True)[:6]
        )
        stats_pills = f"""
            <span class='gh-stat-pill'>Repos <span>{total_repos}</span></span>
            <span class='gh-stat-pill'>Stars <span>{total_stars}</span></span>
            <span class='gh-stat-pill'>Followers <span>{gh_data['followers']}</span></span>
        """

        repo_cards = ""
        for r in repos[:5]:
            name  = r.get("name", "")
            desc  = r.get("description") or "No description provided."
            lang  = r.get("language") or "—"
            stars = r.get("stargazers_count", 0)
            url   = r.get("html_url", "#")
            forks = r.get("forks_count", 0)
            repo_cards += f"""
            <div class='gh-repo-card'>
                <a class='gh-repo-name' href='{url}' target='_blank'>{name}</a>
                <div class='gh-repo-desc'>{desc}</div>
                <div class='gh-repo-meta'>
                    <span class='gh-meta-item'>🔵 {lang}</span>
                    <span class='gh-meta-item'>⭐ {stars}</span>
                    <span class='gh-meta-item'>🍴 {forks}</span>
                </div>
            </div>
            """

        st.markdown(
            f"""
            <div class='gh-panel'>
                <div class='gh-panel-title'>🐙 Live GitHub data · github.com/{GITHUB_USERNAME}</div>
                <div class='gh-stats-row'>{stats_pills}</div>
                <div class='gh-panel-title' style='margin-top:4px'>Top languages</div>
                <div class='gh-stats-row'>{lang_pills}</div>
                <div class='gh-panel-title' style='margin-top:4px'>Recent repositories</div>
                {repo_cards}
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown(
    """
    <div class='footer'>
        <span>Resume · GitHub API · CodeChef · Groq · Llama 3.3 · Streamlit</span>
        <br/>Document-grounded. No hallucinations.
    </div>
    """,
    unsafe_allow_html=True
)
