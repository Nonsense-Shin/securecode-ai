# SecureCode-AI 

SecureCode-AI is an asynchronous AI operational terminal engineered to perform automated static application security testing (SAST). Powered by **FastAPI** and integrated natively with the **Google Gemini 2.5 Flash** engine, the platform ingests raw source code scripts and executes multi-layered logical vulnerability assessments, mapping architectural flaws and outputting precise refactored remediations in real time.

> This is a prototype. The modified and up-to date version is available for comapanies only.

---

## Core Security & Operational Features

### 1. Zero-Leak Token Isolation Architecture
Sensitive infrastructure variables and the `GEMINI_API_KEY` are decoupled entirely from the repository layout. Environment tokens exist purely within volatile system memory at runtime via host configuration variables, preventing remote key extraction vectors and credential leaks.

### 2. In-Memory Stream Processing
Uploaded code payloads are captured and decoded directly within volatile memory buffers using `python-multipart` handling. The application avoids writing target scripts to local block storage, eliminating common local file inclusion (LFI) or unauthorized file execution threats on the host server.

### 3. Contextual Anchor Guardrails
System instructions are hard-coded deep within the backend infrastructure layer. The system enforces strict boundary constraints, rejecting prompt injection attempts, character-override overrides, or queries outside the absolute scope of source code security analysis.

### 4. Direct Static Analysis and Remediations
The analytical model locates complex logical vulnerabilities (e.g., SQL Injection, XSS, Buffer Overflows, Broken Access Controls), maps the flaw's precise execution path, and synthesizes safe, parameter-bound refactored code blocks to close exploitation windows instantly.

---

## Operational Interface Display

<img width="800" height="600" alt="Screenshot 2026-06-21 143501" src="https://github.com/user-attachments/assets/c773d6d5-70c0-4e99-87a2-4acf9b45b566" />


---

## Directory Architecture

```
securecode-ai/
│
├── static/
│   └── index.html          # Unified dark terminal interface (HTML5/CSS3/JS)
│
├── .env                    # Private infrastructure token repository (Git-Ignored)
├── .gitignore              # Strict tracking isolation block
├── main.py                 # FastAPI backend execution kernel & inference router
└── requirements.txt        # Python dependency manifest
```
---
# Local Installation & Deployment
1. Clone the Architecture Matrix
```
git clone https://github.com/Nonsense-Shin/securecode-ai.git
cd securecode-ai
```
2. Establish and Activate the Virtual Perimeter
```
python -m venv .venv
```
# Linux/macOS
`source .venv/bin/activate`

# Windows (CMD)
`.venv\Scripts\activate`

---

3. Deploy Dependencies
```
pip install -r requirements.txt
```
---

4. Configure Local Environment Token 
- Create a `.env` file within the root project directory:

*GEMINI_API_KEY="YOUR_SECRET_GOOGLE_AI_STUDIO_TOKEN"*

---

5. Boot the Asynchronous ASGI Server
```
python -m uvicorn main:app --reload
```

- Navigate to http://127.0.0.1:8000 inside your browser to interface with the terminal workspace.


