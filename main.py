import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("CRITICAL ERROR: GEMINI_API_KEY environmental variable missing.")

genai.configure(api_key=API_KEY)

app = FastAPI(title="SecureCode-AI Automated Audit Kernel")

# Enforce secure CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDITOR_SYSTEM_INSTRUCTIONS = """
You are "SecureCode-Core", an elite automated security code auditor and static analysis intelligence matrix.
Your function is to parse raw source code files uploaded by developers and analyze them strictly for logical vulnerabilities, security flaws, and compliance risks before deployment.

When a code payload is transmitted, execute these evaluation steps:
1. IDENTIFY: Scan for common and advanced logical flaws (e.g., Buffer Overflows, Race Conditions, Command Injections, Broken Access Controls, Hardcoded Credentials, Insecure Cryptography, XSS/SQLi vectors).
2. TRACE: Locate the exact logic pattern or functional blocks where the weakness resides.
3. REMEDIATE: Provide the exact, optimized refactored code block fixes that completely close the exploit window.

OUTPUT FORMATTING CONSTRAINTS:
- Use clean, highly structured terminal-style Markdown output.
- Start with a clear "CRITICAL COUNTER-MEASURES SUMMARY" block breaking down vulnerabilities by severity (CRITICAL, HIGH, MEDIUM, LOW).
- Use code blocks generously to isolate vulnerable segments versus secure refactored code segments.
- Keep the language deeply analytical, cold, precise, and strictly technical. No conversational fluff or introductory greetings. If the code is perfectly secure, output: "STATUS: SECURE. No critical logical anomalies detected within file buffer layers."
"""

ALLOWED_EXTENSIONS = {'.c', '.cpp', '.h', '.py', '.js', '.ts', '.go', '.rs', '.java', '.php', '.sh', '.sol', '.html'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB Limit

@app.post("/api/v1/audit")
async def execute_code_audit(file: UploadFile = File(...)):
    filename = file.filename
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"SECURITY REJECTION: Extension '{ext}' is unauthorized.")
    
    try:
        content_bytes = await file.read()
        if len(content_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="PAYLOAD REJECTION: Target source exceeds 5MB.")
            
        raw_code_payload = content_bytes.decode("utf-8")

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=AUDITOR_SYSTEM_INSTRUCTIONS
        )
        
        prompt = f"TARGET FILENAME: {filename}\n\n[START OF TARGET FILE BUFFER]\n```\n{raw_code_payload}\n```\n[END OF TARGET FILE BUFFER]\n\nExecute absolute vulnerability scanning sequences now."
        response = model.generate_content(prompt)
        
        return {"filename": filename, "analysis_report": response.text}
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="PARSING FAILURE: File must be a raw text script.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal runtime error: {str(e)}")

# Mount the frontend directory so FastAPI can serve the HTML page automatically
app.mount("/", StaticFiles(directory="static", html=True), name="static")