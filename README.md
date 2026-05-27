# AI RAG Portfolio

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-111111?style=for-the-badge)
![GitHub API](https://img.shields.io/badge/GitHub-API-181717?style=for-the-badge&logo=github&logoColor=white)

An interactive AI-powered portfolio assistant for Aditi Garg. The app lets visitors ask natural-language questions about Aditi's resume, projects, GitHub work, competitive programming profile, and technical skills.

Instead of showing a static portfolio page, this project turns career information into a searchable RAG-style experience using Streamlit, Groq, PDF parsing, lightweight retrieval, and live GitHub API data.

## What It Does

- Answers questions about resume, projects, skills, achievements, and GitHub repositories.
- Uses resume and project PDFs as a local knowledge base.
- Retrieves relevant text chunks before sending context to the LLM.
- Pulls public GitHub profile and repository data using the GitHub REST API.
- Includes CodeChef and coding profile context for stronger technical answers.
- Provides a polished Streamlit UI with custom CSS, search chips, and resume download support.
- Uses environment variables for API keys and configuration.

## Tech Stack

| Area | Tools / Libraries |
| --- | --- |
| Frontend / App UI | Streamlit, HTML, CSS |
| Language | Python |
| LLM Provider | Groq |
| Model Config | `llama-3.3-70b-versatile` by default |
| Document Parsing | pypdf |
| Retrieval Logic | Custom chunking and keyword-based relevance scoring |
| External Data | GitHub REST API |
| HTTP Requests | requests |
| Environment Config | python-dotenv |
| Source Control | Git, GitHub |

## Skills Demonstrated

- Generative AI application development
- RAG pipeline design
- Prompt engineering
- LLM context construction
- PDF text extraction
- Information retrieval and chunk ranking
- API integration with GitHub
- Streamlit app development
- Python backend scripting
- Environment variable and secrets management
- UI styling with custom CSS
- Portfolio storytelling for recruiters and hiring teams
- Git/GitHub project publishing workflow

## Project Structure

```text
AI-RAG-Portfolio/
|-- app.py
|-- requirements.txt
|-- README.md
|-- .env.example
|-- .gitignore
`-- data/
    |-- resume.pdf
    `-- projects.pdf
```

## How It Works

1. The app loads resume and project PDFs from the `data/` folder.
2. Text is extracted with `pypdf`.
3. The extracted content is split into smaller chunks.
4. A user asks a question through the Streamlit interface.
5. Relevant chunks are selected using a lightweight retrieval function.
6. GitHub profile and repository data are fetched and added as context.
7. Groq generates a tailored answer using the assembled context.

## Setup

Clone the repository:

```powershell
git clone https://github.com/aditi23garg/AI-RAG-Portfolio.git
cd AI-RAG-Portfolio
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

Add your real values to `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GITHUB_TOKEN=your_github_token_here
```

`GITHUB_TOKEN` is optional. It increases GitHub API rate limits for public profile and repository lookups.

## Run Locally

```powershell
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal.

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `GROQ_API_KEY` | Yes | API key used to call Groq models |
| `GROQ_MODEL` | No | Model name, defaults to `llama-3.3-70b-versatile` |
| `GITHUB_TOKEN` | No | Optional GitHub token for higher API rate limits |

## Highlights

- Built as a real interactive portfolio, not just a static website.
- Uses a RAG-inspired flow to ground answers in actual resume and project documents.
- Combines local documents with live GitHub metadata.
- Keeps secrets out of version control using `.env` and `.gitignore`.
- Designed to help recruiters, hiring managers, and collaborators quickly explore relevant experience.

## Author

**Aditi Garg**

GitHub: [aditi23garg](https://github.com/aditi23garg)
