param (
    [string]$TicketId = "TEST"
)

Write-Host "========================================"
Write-Host "  QA Agent Workflow - Powered by Gemini"
Write-Host "  Ticket: $TicketId"
Write-Host "========================================"
Write-Host ""

# Run the Python agent pipeline
python run-qa-agent.py "$TicketId"
