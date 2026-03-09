# Setup Guide: QA Automation Agents (Gemini Edition)

## What You Need to Install (One Time Only)

### 1. Install Python Dependencies
In the project folder, run:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. Configure the Gemini API Key
This project uses the fast and free **Google Gemini** API.
1. Get a free API key at: https://aistudio.google.com/
2. Open the `.env` file in this project folder.
3. Paste your key inside like this:
```env
GEMINI_API_KEY=your_actual_key_here
```

## How to Run the Agent

### In a terminal, run the agent
```powershell
.\run-qa.ps1 TEST
```

### What Happens
1. The Python runner reads each `agents/*.md` file as a prompt.
2. It sends the prompt + ticket data to the Google Gemini API.
3. The AI generates: ticket summary → test cases → Playwright script.
4. The runner executes the Python Playwright script and opens the browser visibly.
5. A final `test-report.md` is generated automatically.

## Files Generated Per Run
```text
tickets/mock-ticket/
├── raw-ticket.md         # Azure Ticket Agent output
├── ticket-summary.md     # Ticket Summary Agent output (AI-generated)
├── test-cases.md         # Test Case Agent output (AI-generated)
├── _playwright_runner.py # Generated automation script (AI-generated)
├── test-results.md       # Browser test results
├── test-report.md        # Final report (AI-generated)
└── screenshots/          # Failure screenshots
```
