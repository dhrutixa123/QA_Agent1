#!/bin/bash

TICKET_ID=${1:-TEST}

echo "========================================"
echo "  QA Agent Workflow — Powered by Gemini"
echo "  Ticket: $TICKET_ID"
echo "========================================"
echo ""

# Run the Python agent pipeline
python run-qa-agent.py "$TICKET_ID"
