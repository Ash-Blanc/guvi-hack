#!/bin/bash

# Configuration
API_URL="${API_URL:-http://localhost:8001/analyze}"
API_KEY="${API_KEY:-test-key}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

function print_usage() {
    echo "Usage: $0 [scenario]"
    echo "Scenarios:"
    echo "  vikram   - Test Vikram persona (GST/Business scam)"
    echo "  priya    - Test Priya persona (Urgent/Bank scam)"
    echo "  suresh   - Test Suresh persona (International/NRI scam)"
    echo "  custom   - specific message (usage: $0 custom \"your message\")"
    echo ""
    echo "Example: $0 vikram"
}

function send_request() {
    local session_id=$1
    local message=$2
    local history=${3:-"[]"}
    
    echo -e "${BLUE}Sending request to $API_URL...${NC}"
    echo "Message: $message"
    
    local response=$(curl -s -X POST "$API_URL" \
      -H "Content-Type: application/json" \
      -H "x-api-key: $API_KEY" \
      -d "{
        \"sessionId\": \"$session_id\",
        \"message\": {
            \"sender\": \"scammer\",
            \"text\": \"$message\",
            \"timestamp\": $(date +%s)
        },
        \"conversationHistory\": $history,
        \"metadata\": {
            \"channel\": \"SMS\",
            \"language\": \"English\",
            \"locale\": \"IN\"
        }
      }")
    
    # Pretty print with jq if available, otherwise raw JSON
    if command -v jq &> /dev/null; then
        echo "$response" | jq .
    else
        echo "$response"
    fi
    echo ""
}

SCENARIO=$1
MESSAGE=$2

case $SCENARIO in
    vikram)
        echo -e "${GREEN}=== Testing VIKRAM Persona (Business Scam) ===${NC}"
        send_request "test-vikram" "Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty."
        ;;
        
    priya)
        echo -e "${GREEN}=== Testing PRIYA Persona (Urgent Scam) ===${NC}"
        send_request "test-priya" "URGENT: Your HDFC account will expire within 24 hours. Click here to verify."
        ;;
        
    suresh)
        echo -e "${GREEN}=== Testing SURESH Persona (NRI Scam) ===${NC}"
        send_request "test-suresh" "Sir your international wire transfer of $5000 is blocked. Need KYC update."
        ;;
        
    custom)
        if [ -z "$MESSAGE" ]; then
            echo "Error: Message required for custom scenario"
            exit 1
        fi
        send_request "test-custom" "$MESSAGE"
        ;;
        
    *)
        print_usage
        exit 1
        ;;
esac
