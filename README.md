# Aditi AI Portfolio

An interactive Streamlit portfolio assistant that uses Groq, resume/project PDFs, and public GitHub data to answer questions about Aditi's work.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your real `GROQ_API_KEY` to `.env`. `GITHUB_TOKEN` is optional.

## Run

```powershell
streamlit run app.py
```
