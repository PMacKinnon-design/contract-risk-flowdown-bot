
# AI Contract Risk & Flowdown BOT

Upload a contract file (TXT or PDF) and receive an AI-powered risk review and flowdown clause generator. The BOT identifies high-risk areas and regulatory flowdown obligations using keyword triggers and text analysis.

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features
- PDF and TXT support
- Risk scoring of key clauses (indemnity, termination, etc.)
- Flowdown clause identification from FAR/DFARS and internal policies
- CSV export of results
