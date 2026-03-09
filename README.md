# QA Automation AI Agents

This repository contains entirely Markdown-based AI agents to automate QA tasks from Azure DevOps tickets to test execution and reporting.

## Installation

To set up the repository on a new system:
1. Ensure Python is installed (3.9+ recommended).
2. Install the required dependencies from the provided text file:
   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```
3. Follow the instructions in `SETUP-GEMINI.md` to configure your API keys.

## How to Configure

### 1. Enable Mock Mode (Optional)
This allows the system to be tested locally without Azure DevOps or a real application.
Edit `config/system-config.md`:
```markdown
Mock Mode: ON
```

### 2. Configure Azure Credentials (Production)
Edit `config/azure-config.md` to add your Azure Organization, Project, PAT, and Base URL.

### 3. Configure Test Data
Edit `config/test-data.md` to define application URLs and login credentials for both Mock and Production environments.

## How to Start Automation

This system is entirely AI-Agent driven. To start the automation, simply tell the AI Agent:

```bash
.\run-qa.ps1 TICKET_ID
```

The AI will then:
1. Locate the agent instructions in the `agents/` folder.
2. Follow the sequence defined in `workflows/qa-workflow.md`.
3. Use its internal tools to fetch tickets, generate test cases, and execute browser automation.
4. Provide you with the final Markdown report.


This will trigger the multi-agent workflow:
1. **Azure Ticket Agent**: Fetches ticket details or uses the mock ticket.
2. **Ticket Summary Agent**: Summarizes the feature and requirements.
3. **Test Case Generator Agent**: Creates structured QA test cases.
4. **Browser Automation Agent**: Runs the test cases via Playwright against the production or mock website.
5. **Test Report Agent**: Generates the final execution report.
