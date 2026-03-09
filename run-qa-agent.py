#!/usr/bin/env python3
"""
QA Automation Agent Runner — Powered by Google Gemini
This script reads your Markdown agent files and uses the Gemini API
to generate ticket summaries, test cases, and reports autonomously.
"""

import os
import sys
import json
import subprocess
import re
import requests
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
load_dotenv()  # Load variables from .env file

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"  # The fast, free tier model
BASE_DIR = Path(__file__).parent
AGENTS_DIR = BASE_DIR / "agents"
CONFIG_DIR = BASE_DIR / "config"
MOCK_DATA_DIR = BASE_DIR / "mock-data"

# ─────────────────────────────────────────────
# HELPER: Call Gemini API
# ─────────────────────────────────────────────
def call_gemini(system_prompt: str, user_message: str) -> str:
    """Call the Google Gemini API and return the generated text."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        print("\n  [ERROR] ❌ GEMINI_API_KEY is missing or invalid!")
        print("  Please open the '.env' file in your project folder and add your key.")
        print("  Get a free key at: https://aistudio.google.com/")
        sys.exit(1)

    print(f"  [AI Brain] 🤖 Calling Gemini ({GEMINI_MODEL})...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[user_message],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.2, # Keep hallucination low for coding tasks
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"\n  [ERROR] ❌ Gemini API Request Failed: {e}")
        sys.exit(1)

# ─────────────────────────────────────────────
# HELPER: Read a Markdown file
# ─────────────────────────────────────────────
def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ─────────────────────────────────────────────
# HELPER: Write a Markdown file
# ─────────────────────────────────────────────
def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ─────────────────────────────────────────────
# AGENT 1: Azure Ticket Agent
# ─────────────────────────────────────────────
def run_azure_ticket_agent(ticket_dir: Path, is_mock: bool):
    print("\nStep 1: Fetch Ticket (Azure Ticket Agent)")
    agent_prompt = read_file(AGENTS_DIR / "azure-ticket-agent.md")
    raw_output = ticket_dir / "raw-ticket.md"

    if is_mock:
        source = MOCK_DATA_DIR / "sample-ticket.md"
        ticket_data = read_file(source)
        user_msg = f"Mock Mode is ON. Here is the raw ticket data:\n\n{ticket_data}\n\nPlease confirm you have processed this ticket and output it in the raw-ticket.md format."
        result = call_gemini(agent_prompt, user_msg)
        write_file(raw_output, f"# Raw Ticket (MOCK)\n\n{result}")
    else:
        # Fetch from Azure DevOps REST API
        print(f"  [Azure] ☁️ Fetching Ticket ID: {ticket_dir.name}...")
        azure_config = read_file(CONFIG_DIR / "azure-config.md")
        
        # Simple extraction from markdown config format
        def get_cfg(key):
            match = re.search(f"{key}:\\s*(.*)", azure_config, re.IGNORECASE)
            return match.group(1).strip() if match else ""

        org = get_cfg("Azure Organization")
        project = get_cfg("Project Name")
        pat = get_cfg("Personal Access Token")
        
        url = f"https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{ticket_dir.name}?$expand=fields&api-version=7.1"
        
        try:
            from requests.auth import HTTPBasicAuth
            resp = requests.get(url, auth=HTTPBasicAuth('', pat), timeout=30)
            resp.raise_for_status()
            data = resp.json()
            fields = data.get("fields", {})
            
            content = f"# Ticket: {data.get('id')} - {fields.get('System.Title')}\n\n"
            content += f"## Description\n{fields.get('System.Description', 'N/A')}\n\n"
            content += f"## User Story\n{fields.get('Microsoft.VSTS.Scheduling.StoryPoints', 'N/A')} Points\n\n"
            content += f"## Acceptance Criteria\n{fields.get('Microsoft.VSTS.Common.AcceptanceCriteria', 'N/A')}\n"
            
            write_file(raw_output, content)
            print(f"  [OK] Fetched dynamic data from Azure.")
        except Exception as e:
            print(f"  [ERROR] ❌ Failed to fetch from Azure: {e}")
            print("  Falling back to manual prompt processing...")
            user_msg = f"Fetch the ticket {ticket_dir.name} from Azure DevOps using the config provided."
            result = call_gemini(agent_prompt, user_msg)
            write_file(raw_output, f"# Raw Ticket (AI Search Attempt)\n\n{result}")

    print(f"  [OK] Output: {raw_output}")

# ─────────────────────────────────────────────
# AGENT 2: Ticket Summary Agent
# ─────────────────────────────────────────────
def run_ticket_summary_agent(ticket_dir: Path):
    print("\nStep 2: Summarize Ticket (Ticket Summary Agent)")
    agent_prompt = read_file(AGENTS_DIR / "ticket-summary-agent.md")
    raw_ticket = read_file(ticket_dir / "raw-ticket.md")
    summary_output = ticket_dir / "ticket-summary.md"

    user_msg = f"Here is the raw ticket data:\n\n{raw_ticket}\n\nPlease summarize this ticket following your instructions."
    result = call_gemini(agent_prompt, user_msg)
    write_file(summary_output, result)
    print(f"  [OK] Output: {summary_output}")

# ─────────────────────────────────────────────
# AGENT 3: Test Case Generator Agent
# ─────────────────────────────────────────────
def run_testcase_agent(ticket_dir: Path):
    print("\nStep 3: Generate Test Cases (Test Case Generator Agent)")
    agent_prompt = read_file(AGENTS_DIR / "testcase-agent.md")
    summary = read_file(ticket_dir / "ticket-summary.md")
    testcase_output = ticket_dir / "test-cases.md"

    user_msg = f"Here is the ticket summary:\n\n{summary}\n\nGenerate detailed QA test cases as a Markdown table following your instructions. Output ONLY the Markdown table, nothing else."
    result = call_gemini(agent_prompt, user_msg)
    write_file(testcase_output, f"# QA Test Cases\n\n{result}")
    print(f"  [OK] Output: {testcase_output}")

# ─────────────────────────────────────────────
# HELPER: Dynamic DOM Scraper using Playwright
# Runs Playwright in a subprocess to avoid Python 3.14 + Windows
# asyncio event loop issues with sync_playwright inline usage.
# ─────────────────────────────────────────────
def scrape_page_dom(url: str) -> str:
    """
    Visits the given URL using a headless Playwright browser (subprocess),
    extracts all interactive DOM elements (inputs, buttons, links),
    triggers form validation errors (empty submit + invalid email),
    and returns a structured text report of the real DOM.
    """
    print(f"  [DOM Scraper] 🔍 Visiting {url} with Playwright...")

    # Build the standalone scraper script as a string
    # Using <<<DELIM>>> style to avoid f-string conflicts
    scraper_lines = [
        "from playwright.sync_api import sync_playwright",
        f"url = {repr(url)}",
        "report = []",
        "try:",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=True)",
        "        page = browser.new_page()",
        "        page.goto(url, wait_until='domcontentloaded', timeout=30000)",
        "        page.wait_for_timeout(2000)",
        "        report.append(f'=== LIVE DOM SCRAPE: {url} ===')",
        "        report.append(f'--- Page Title: {page.title()} ---')",
        "        report.append(f'--- Final URL: {page.url} ---')",
        "",
        "        # Inputs",
        "        report.append('\\n=== INPUT FIELDS ===')",
        "        for el in page.query_selector_all('input'):",
        "            d = {k: el.get_attribute(k) or '' for k in ['id','name','type','placeholder','class','data-testid','value']}",
        "            d['tag'] = 'input'",
        "            report.append(str({k: v for k, v in d.items() if v}))",
        "",
        "        # Buttons",
        "        report.append('\\n=== BUTTONS ===')",
        "        for el in page.query_selector_all('button'):",
        "            d = {'tag':'button','type':el.get_attribute('type') or '','text':el.inner_text().strip(),'class':el.get_attribute('class') or ''}",
        "            report.append(str({k: v for k, v in d.items() if v}))",
        "",
        "        # Links",
        "        report.append('\\n=== LINKS ===')",
        "        for el in page.query_selector_all('a'):",
        "            text = el.inner_text().strip()",
        "            href = el.get_attribute('href') or ''",
        "            if text or href:",
        "                report.append(str({'tag':'a','text':text,'href':href,'class':el.get_attribute('class') or ''}))",
        "",
        "        # Empty form submit to capture validation errors",
        "        report.append('\\n=== VALIDATION ERRORS (empty form submit) ===')",
        "        submit = page.query_selector(\"button[type='submit'], input[type='submit']\")",
        "        if submit:",
        "            submit.click()",
        "            page.wait_for_timeout(2000)",
        "            sels = '.invalid-feedback, .error-message, .alert-danger, [class*=\"error\"]'",
        "            for err in page.query_selector_all(sels):",
        "                txt = err.inner_text().strip()",
        "                if txt:",
        "                    parent = err.evaluate(\"el => el.parentElement ? el.parentElement.className : ''\")",
        "                    report.append(f\"  Error: '{txt}' | parent_class: '{parent}'\")",
        "",
        "        # Invalid email to capture format errors",
        "        report.append('\\n=== VALIDATION ERRORS (invalid email format) ===')",
        "        page.goto(url, wait_until='domcontentloaded', timeout=20000)",
        "        page.wait_for_timeout(1500)",
        "        email_el = page.query_selector(\"input[id*='email'], input[name*='email'], input[placeholder*='Email']\")",
        "        if email_el:",
        "            email_el.fill('invalid-email')",
        "        submit2 = page.query_selector(\"button[type='submit'], input[type='submit']\")",
        "        if submit2:",
        "            submit2.click()",
        "            page.wait_for_timeout(2000)",
        "            sels2 = '.invalid-feedback, .error-message, [class*=\"error\"]'",
        "            for err in page.query_selector_all(sels2):",
        "                txt = err.inner_text().strip()",
        "                if txt:",
        "                    parent = err.evaluate(\"el => el.parentElement ? el.parentElement.className : ''\")",
        "                    report.append(f\"  Error: '{txt}' | parent_class: '{parent}'\")",
        "",
        "        browser.close()",
        "except Exception as e:",
        "    report.append(f'[DOM SCRAPER ERROR] {e}')",
        "print('DOM_SCRAPE_RESULT_START')",
        "print('\\n'.join(report))",
        "print('DOM_SCRAPE_RESULT_END')",
    ]
    scraper_script = "\n".join(scraper_lines)

    tmp_scraper = BASE_DIR / "_tmp_dom_scraper.py"
    try:
        write_file(tmp_scraper, scraper_script)
        result = subprocess.run(
            ["python", str(tmp_scraper)],
            capture_output=True, text=True, timeout=90
        )
        output = result.stdout + result.stderr

        # Extract the bounded report from stdout
        if "DOM_SCRAPE_RESULT_START" in output and "DOM_SCRAPE_RESULT_END" in output:
            start = output.index("DOM_SCRAPE_RESULT_START") + len("DOM_SCRAPE_RESULT_START")
            end   = output.index("DOM_SCRAPE_RESULT_END")
            dom_report = output[start:end].strip()
        else:
            dom_report = output or "[DOM scraper produced no output]"

        print("  [DOM Scraper] ✅ DOM scrape complete.")
        return dom_report

    except subprocess.TimeoutExpired:
        print("  [WARNING] DOM scraper timed out after 90s.")
        return "[DOM SCRAPER ERROR] Timed out after 90s"
    except Exception as e:
        print(f"  [WARNING] DOM scraper failed: {e}")
        return f"[DOM SCRAPER ERROR] {e}"
    finally:
        if tmp_scraper.exists():
            tmp_scraper.unlink()

# ─────────────────────────────────────────────
# AGENT 4: Page Analyzer Agent
# ─────────────────────────────────────────────
def run_page_analyzer_agent(ticket_dir: Path, is_mock: bool):
    print("\nStep 4: Analyze Page Selectors (Page Analyzer Agent)")
    
    agent_prompt = read_file(AGENTS_DIR / "page-analyzer-agent.md")
    summary = read_file(ticket_dir / "ticket-summary.md")
    test_cases = read_file(ticket_dir / "test-cases.md")

    selectors_output = ticket_dir / "page-selectors.md"

    # Determine which URL to scrape
    app_url = "https://www.saucedemo.com" if is_mock else "https://stellar.annaizu.com/login"

    # ── STEP A: Actually visit the page and extract real DOM data ──
    live_dom = scrape_page_dom(app_url)

    # ── STEP B: Feed real DOM data to Gemini to produce the selector table ──
    user_msg = f"""You have been given REAL DOM DATA scraped directly from the live website using a headless Playwright browser.

Do NOT guess selectors. Use ONLY the element data provided below.

Application URL: {app_url}

Feature Summary:
{summary}

Test Cases:
{test_cases}

--- LIVE DOM DATA (scraped from real browser) ---
{live_dom}
--- END OF LIVE DOM DATA ---

Instructions:
1. Map each UI element from the test cases to a selector from the LIVE DOM DATA above.
2. Pick the most reliable selector in this priority: #id > input[name=...] > [data-testid] > stable CSS class > text/href
3. For error messages: use the exact error text from the DOM data above, and use the parent class to form the CSS selector.
4. Do NOT invent or guess any selector that is not in the DOM data.

Generate a selector table following your instructions.
Output ONLY the Markdown table.
"""

    result = call_gemini(agent_prompt, user_msg)
    write_file(selectors_output, result)

    print(f"  [OK] Output: {selectors_output}")

# ─────────────────────────────────────────────
# AGENT 5: Browser Automation Agent (Playwright)
# ─────────────────────────────────────────────
def run_browser_agent(ticket_dir: Path, is_mock: bool):
    print("\nStep 5: Run Browser Automation (Browser Agent)")
    
    test_cases_content = read_file(ticket_dir / "test-cases.md")
    selectors_content = read_file(ticket_dir / "page-selectors.md")
    raw_test_data = read_file(CONFIG_DIR / "test-data.md")
    
    # Extract only the relevant environment block to prevent AI credential confusion
    if is_mock:
        match = re.search(r"Valid Login \(Mock\)(.*?)Valid Login \(Production\)", raw_test_data, re.DOTALL | re.IGNORECASE)
        test_data = "Valid Credentials:\n" + match.group(1).strip() if match else raw_test_data
    else:
        match = re.search(r"Valid Login \(Production\)(.*)", raw_test_data, re.DOTALL | re.IGNORECASE)
        test_data = "Valid Credentials:\n" + match.group(1).strip() if match else raw_test_data

    screenshots_dir = ticket_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Ask the AI to generate a Playwright script from the Markdown table
    agent_prompt = read_file(AGENTS_DIR / "browser-agent.md")
    app_url = "https://www.saucedemo.com" if is_mock else "https://stellar.annaizu.com"
    user_msg = f"""Generate a Python Playwright script that executes the following test cases.

Application URL: {app_url}

Test Data:
{test_data}

Page Selectors:
{selectors_content}

Test Cases:
{test_cases_content}

IMPORTANT INSTRUCTIONS:
1. Parse each row of the Markdown table as a separate test case.
2. Use selectors from the Page Selectors table when generating Playwright commands.
3. Use sync_playwright and headless=False so the browser is visible.
4. Add slow_mo=500 delay between actions.
5. Take a screenshot on any failure to: {screenshots_dir.as_posix()}/TC_ID-error.png
6. Print [PASS] or [FAIL] for each test case.
7. At the end print JSON summary like: {{"results":[{{"id":"TC-001","status":"PASS"}}]}}
8. Output ONLY raw Python code.
"""
    
    playwright_script = call_gemini(agent_prompt, user_msg)
    
    # Save and run the script
    script_path = ticket_dir / "_playwright_runner.py"
    # Extract code from markdown fences if model added conversational text
    code_match = re.search(r"```(?:python)?(.*?)```", playwright_script, re.DOTALL | re.IGNORECASE)
    if code_match:
        playwright_script = code_match.group(1).strip()
    else:
        playwright_script = re.sub(r'^(?:Sure|Here|Great|Okay|Ok)[^\n]*\n+', '', playwright_script, flags=re.IGNORECASE).strip()
        playwright_script = re.sub(r"```(?:python)?|```", "", playwright_script).strip()
        
    write_file(script_path, playwright_script)
    
    # Sanity check: Ensure the output actually looks like a Python Playwright script
    if "playwright" not in playwright_script.lower() and "def " not in playwright_script:
        print("  [ERROR] ❌ The AI generated invalid code (not a Python script).")
        print(f"  See the generated output here: {script_path}")
        return 0, 0, 0
    
    print("  [AI Brain] 🌐 Launching Playwright browser...")
    try:
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True, text=True, timeout=300
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired as e:
        output = f"[ERROR] Playwright script timed out after 300 seconds.\n{e.stdout}\n{e.stderr}"
    except Exception as e:
        output = f"[ERROR] Playwright script execution failed:\n{str(e)}"
    print(output)
    
    # Extract JSON results if present
    results_data = []
    try:
        lines = output.strip().split("\n")
        for line in reversed(lines):
            line = line.strip()
            if line.startswith("{") and '"results"' in line and line.endswith("}"):
                results_data = json.loads(line)["results"]
                break
                
        if not results_data:
            json_match = re.search(r'\{[\s\n]*"results"[\s\n]*:[\s\n]*\[.*\][\s\n]*\}', output, re.DOTALL | re.IGNORECASE)
            if json_match:
                results_data = json.loads(json_match.group())["results"]
    except Exception as e:
        print(f"  [WARNING] Could not parse test JSON output: {e}")
        pass

    # Write test results
    results_md = "# Playwright Test Execution Results\n\n"
    results_md += "| Test Case ID | Status | Failure Reason |\n"
    results_md += "|---|---|---|\n"
    
    passed = 0
    failed = 0
    for r in results_data:
        status = r.get("status", "UNKNOWN")
        reason = r.get("reason", "N/A") if status == "FAIL" else "N/A"
        results_md += f"| {r['id']} | {status} | {reason} |\n"
        if status == "PASS": passed += 1
        else: failed += 1

    if not results_data:
        results_md += "| N/A | Script ran - check console output | N/A |\n"

    write_file(ticket_dir / "test-results.md", results_md)
    print(f"  [OK] Results: {ticket_dir}/test-results.md")

    return passed, failed, len(results_data)

# ─────────────────────────────────────────────
# AGENT 6: Report Agent
# ─────────────────────────────────────────────
def run_report_agent(ticket_dir: Path, passed: int, failed: int, total: int):
    print("\nStep 6: Generate Report (Report Agent)")
    agent_prompt = read_file(AGENTS_DIR / "report-agent.md")
    test_cases = read_file(ticket_dir / "test-cases.md")
    test_results = read_file(ticket_dir / "test-results.md")
    
    pass_rate = round((passed / total) * 100) if total > 0 else 0
    user_msg = f"""Generate a final QA Markdown report based on the following:

Test Cases:
{test_cases}

Test Results:
{test_results}

Summary Stats:
- Total: {total}
- Passed: {passed}
- Failed: {failed}
- Pass Rate: {pass_rate}%

Output ONLY the Markdown report."""
    
    result = call_gemini(agent_prompt, user_msg)
    write_file(ticket_dir / "test-report.md", result)
    print(f"  [OK] Report: {ticket_dir}/test-report.md")

# ─────────────────────────────────────────────
# MAIN ORCHESTRATOR
# ─────────────────────────────────────────────
def main():
    ticket_id = sys.argv[1] if len(sys.argv) > 1 else "TEST"

    # Read mock mode from config
    system_config = read_file(CONFIG_DIR / "system-config.md")
    is_mock = "mock mode: on" in system_config.lower()

    ticket_folder = "mock-ticket" if is_mock else ticket_id
    ticket_dir = BASE_DIR / "tickets" / ticket_folder
    ticket_dir.mkdir(parents=True, exist_ok=True)

    mode_label = "MOCK MODE (Gemini API)" if is_mock else f"LIVE MODE — Ticket: {ticket_id}"
    print("=" * 50)
    print(f"  QA Agent Workflow — {mode_label}")
    print(f"  Model: Google / {GEMINI_MODEL}")
    print("=" * 50)

    run_azure_ticket_agent(ticket_dir, is_mock)
    run_ticket_summary_agent(ticket_dir)
    run_testcase_agent(ticket_dir)
    run_page_analyzer_agent(ticket_dir, is_mock)
    passed, failed, total = run_browser_agent(ticket_dir, is_mock)
    run_report_agent(ticket_dir, passed, failed, total)

    print("\n" + "=" * 50)
    print("  ✅ Workflow Complete!")
    print(f"  Results folder: tickets/{ticket_folder}/")
    print("=" * 50)

if __name__ == "__main__":
    main()
