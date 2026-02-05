#!/bin/bash

# Multi-Turn API Verification Script
# Tests 4 distinct scenarios: GST Scam, Job Scam, Lottery Scam, and Safe Message

API_URL="${API_URL:-http://localhost:8001/analyze}"
API_KEY="${API_KEY:-test-key}"
DATE_TAG=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="verification_results_${DATE_TAG}.txt"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${GREEN}=== Multi-Turn API Verification Started ===${NC}"
echo "Target URL: $API_URL"
echo "Results file: $OUTPUT_FILE"
echo ""

# Initialize log
echo "=== API Verification Log - $DATE_TAG ===" > "$OUTPUT_FILE"

# Function to send a message
# Usage: send_turn <scenario_name> <turn_num> <sender> <message> <history_json> <session_id>
send_turn() {
    local scenario="$1"
    local turn="$2"
    local sender="$3"
    local msg="$4"
    local history="$5"
    local session_id="$6"
    
    echo -e "${BLUE}[$scenario] Turn $turn ($sender):${NC} $msg"
    
    # Log request
    echo "[$scenario] Turn $turn - $sender: $msg" >> "$OUTPUT_FILE"
    
    local payload=$(cat <<EOF
{
  "sessionId": "$session_id",
  "message": {
      "sender": "$sender",
      "text": "$msg",
      "timestamp": $(date +%s)000
  },
  "conversationHistory": $history,
  "metadata": {
      "source": "verification_script",
      "scenario": "$scenario"
  }
}
EOF
)
    
    local start_time=$(date +%s%N)
    local response=$(curl -s -X POST "$API_URL" \
      -H "Content-Type: application/json" \
      -H "x-api-key: $API_KEY" \
      -d "$payload")
    local end_time=$(date +%s%N)
    local duration=$(( ($end_time - $start_time) / 1000000 ))

    # Extract clean reply (removing newlines/escapes for display)
    local reply=$(echo "$response" | grep -o '"reply":"[^"]*"' | cut -d'"' -f4 | sed 's/\\n/ /g')
    local is_scam=$(echo "$response" | grep -o 'is_scam' | wc -l) # Basic check if internal logic flagged it (not directly in response usually, but inferred)
    
    # In a real response, 'reply' is what we want. 
    # If the agent is working, it should return a persona-based reply for scams.
    
    echo -e "${YELLOW}Agent Reponse (${duration}ms):${NC} $reply"
    echo "Agent Response: $reply" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo ""

    # Return the reply for history building
    echo "$reply"
}

# ==============================================================================
# SCENARIO 1: GST Scam (Vikram Persona)
# ==============================================================================
run_scenario_1() {
    local SID="sess_gst_$DATE_TAG"
    local SCENARIO="GST_SCAM"
    local HIST="[]"
    
    echo -e "${CYAN}--- Scenario 1: GST Scam ---${NC}"
    
    # Turn 1
    local MSG1="Your GST registration is blocked due to unpaid taxes of Rs 45,000. Pay immediately."
    local AGENT1=$(send_turn "$SCENARIO" 1 "scammer" "$MSG1" "$HIST" "$SID")
    
    # Turn 2
    HIST="[{\"sender\":\"scammer\",\"text\":\"$MSG1\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$AGENT1\",\"timestamp\":$(date +%s)000}]"
    local MSG2="Sir if you don't pay to UPI id tax.gov@okhdfc within 10 mins, police team will be dispatched."
    local AGENT2=$(send_turn "$SCENARIO" 2 "scammer" "$MSG2" "$HIST" "$SID")
    
    # Turn 3
    HIST="[{\"sender\":\"scammer\",\"text\":\"$MSG1\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$AGENT1\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"$MSG2\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$AGENT2\",\"timestamp\":$(date +%s)000}]"
    local MSG3="Be quick sir. Send screenshot to 9898989898 after payment."
    local AGENT3=$(send_turn "$SCENARIO" 3 "scammer" "$MSG3" "$HIST" "$SID")
}

# ==============================================================================
# SCENARIO 2: Job Offer Scam (Likely Student/Job Seeker Persona)
# ==============================================================================
run_scenario_2() {
    local SID="sess_job_$DATE_TAG"
    local SCENARIO="JOB_SCAM"
    local HIST="[]"
    
    echo -e "${CYAN}--- Scenario 2: Job Offer Scam ---${NC}"
    
    # Turn 1
    local MSG1="Hi, we reviewed your profile. We are offering you a Part-Time Job working from home. Salary Rs 5000-8000 per day."
    local AGENT1=$(send_turn "$SCENARIO" 1 "scammer" "$MSG1" "$HIST" "$SID")
    
    # Turn 2
    HIST="[{\"sender\":\"scammer\",\"text\":\"$MSG1\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$AGENT1\",\"timestamp\":$(date +%s)000}]"
    local MSG2="No experience needed. Just need to like YouTube videos. Join our Telegram channel: t.me/easyjobs123 for training."
    local AGENT2=$(send_turn "$SCENARIO" 2 "scammer" "$MSG2" "$HIST" "$SID")
    
    # Turn 3
    HIST="[{\"sender\":\"scammer\",\"text\":\"$MSG1\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$AGENT1\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"$MSG2\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$AGENT2\",\"timestamp\":$(date +%s)000}]"
    local MSG3="To start, you must pay registration fee of Rs 2000 which is refundable."
    local AGENT3=$(send_turn "$SCENARIO" 3 "scammer" "$MSG3" "$HIST" "$SID")
}

# ==============================================================================
# SCENARIO 3: Lottery Scam (Likely Retired/Elderly Persona or Greedy Youth)
# ==============================================================================
run_scenario_3() {
    local SID="sess_lotto_$DATE_TAG"
    local SCENARIO="LOTTERY_SCAM"
    local HIST="[]"
    
    echo -e "${CYAN}--- Scenario 3: Lottery Scam ---${NC}"
    
    # Turn 1
    local MSG1="CONGRATULATIONS! You have won Rs 2 Crores in KBC Lucky Draw."
    local AGENT1=$(send_turn "$SCENARIO" 1 "scammer" "$MSG1" "$HIST" "$SID")
    
    # Turn 2
    HIST="[{\"sender\":\"scammer\",\"text\":\"$MSG1\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$AGENT1\",\"timestamp\":$(date +%s)000}]"
    local MSG2="To claim your prize, call Rana Pratap immediately at +91-9000000000."
    local AGENT2=$(send_turn "$SCENARIO" 2 "scammer" "$MSG2" "$HIST" "$SID")
}

# ==============================================================================
# SCENARIO 4: Safe Message (Control - Expecting polite dismissal)
# ==============================================================================
run_scenario_4() {
    local SID="sess_safe_$DATE_TAG"
    local SCENARIO="SAFE_MSG"
    local HIST="[]"
    
    echo -e "${CYAN}--- Scenario 4: Safe Message ---${NC}"
    
    local MSG1="Hey, result is out for the semester. Check the college portal."
    local AGENT1=$(send_turn "$SCENARIO" 1 "scammer" "$MSG1" "$HIST" "$SID")
    
    echo -e "${GREEN}Expectation for scenario 4: Agent should NOT engage as a Persona, but reply normally stating it's safe.${NC}"
}

# Run all scenarios
run_scenario_1
run_scenario_2
run_scenario_3
run_scenario_4

echo -e "${GREEN}=== Verification Complete ===${NC}"
echo "Results saved to $OUTPUT_FILE"
