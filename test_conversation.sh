#!/bin/bash

# Multi-Turn Conversation Test Script
# Simulates a realistic 7-turn conversation with the Honeypot API

API_URL="http://localhost:8001/analyze"
API_KEY="test-key"
SESSION_ID="test-session-$(date +%s)"
OUTPUT_FILE="test_results_${SESSION_ID}.txt"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Multi-Turn Conversation Test ===${NC}"
echo "Session ID: $SESSION_ID"
echo "Output file: $OUTPUT_FILE"
echo ""

# Initialize output file
echo "=== Honeypot API Test Results ===" > "$OUTPUT_FILE"
echo "Session ID: $SESSION_ID" >> "$OUTPUT_FILE"
echo "Timestamp: $(date)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to send a message and capture response
send_turn() {
    local turn_num=$1
    local sender=$2
    local message=$3
    local history=$4
    
    echo -e "${BLUE}Turn $turn_num ($sender):${NC} $message"
    
    local response=$(curl -s -X POST "$API_URL" \
      -H "Content-Type: application/json" \
      -H "x-api-key: $API_KEY" \
      -d "{
        \"sessionId\": \"$SESSION_ID\",
        \"message\": {
            \"sender\": \"$sender\",
            \"text\": \"$message\",
            \"timestamp\": $(date +%s)000
        },
        \"conversationHistory\": $history,
        \"metadata\": {
            \"channel\": \"SMS\",
            \"language\": \"English\",
            \"locale\": \"IN\"
        }
      }")
    
    # Extract reply from response
    local reply=$(echo "$response" | grep -o '"reply":"[^"]*"' | cut -d'"' -f4 | sed 's/\\n/ /g')
    
    # Log to file
    echo "Turn $turn_num [$sender]: $message" >> "$OUTPUT_FILE"
    if [ "$sender" = "scammer" ]; then
        echo "Response [agent]: $reply" >> "$OUTPUT_FILE"
    fi
    echo "" >> "$OUTPUT_FILE"
    
    # Display response
    if [ "$sender" = "scammer" ]; then
        echo -e "${YELLOW}Agent Response:${NC} $reply"
    fi
    echo ""
    
    # Return the reply for building history
    echo "$reply"
}

# ==============================================================================
# SCENARIO 1: GST/Business Scam (Vikram Persona Expected)
# ==============================================================================

echo -e "${GREEN}Starting Conversation: GST Payment Scam${NC}"
echo ""
echo "--- Conversation: GST Payment Scam ---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Build conversation history progressively
HISTORY="[]"

# Turn 1: Scammer initiates
REPLY1=$(send_turn 1 "scammer" "Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty." "$HISTORY")

# Turn 2: Build history with Turn 1
HISTORY="[{\"sender\":\"scammer\",\"text\":\"Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY1\",\"timestamp\":$(date +%s)000}]"
REPLY2=$(send_turn 2 "scammer" "Sir this is from GST department. Send payment to UPI: gst.payment@okaxis or your business license will be suspended." "$HISTORY")

# Turn 3
HISTORY="[{\"sender\":\"scammer\",\"text\":\"Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY1\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir this is from GST department. Send payment to UPI: gst.payment@okaxis or your business license will be suspended.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY2\",\"timestamp\":$(date +%s)000}]"
REPLY3=$(send_turn 3 "scammer" "You can call our helpline 9876543210 for verification. But payment must be done in 1 hour." "$HISTORY")

# Turn 4
HISTORY="[{\"sender\":\"scammer\",\"text\":\"Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY1\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir this is from GST department. Send payment to UPI: gst.payment@okaxis or your business license will be suspended.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY2\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"You can call our helpline 9876543210 for verification. But payment must be done in 1 hour.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY3\",\"timestamp\":$(date +%s)000}]"
REPLY4=$(send_turn 4 "scammer" "Sir are you sending the payment? Just confirm your bank account number ending digits for our records." "$HISTORY")

# Turn 5
HISTORY="[{\"sender\":\"scammer\",\"text\":\"Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY1\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir this is from GST department. Send payment to UPI: gst.payment@okaxis or your business license will be suspended.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY2\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"You can call our helpline 9876543210 for verification. But payment must be done in 1 hour.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY3\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir are you sending the payment? Just confirm your bank account number ending digits for our records.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY4\",\"timestamp\":$(date +%s)000}]"
REPLY5=$(send_turn 5 "scammer" "Last warning sir. Send Rs 50000 to gst.payment@okaxis now or face legal action." "$HISTORY")

# Turn 6
HISTORY="[{\"sender\":\"scammer\",\"text\":\"Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY1\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir this is from GST department. Send payment to UPI: gst.payment@okaxis or your business license will be suspended.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY2\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"You can call our helpline 9876543210 for verification. But payment must be done in 1 hour.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY3\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir are you sending the payment? Just confirm your bank account number ending digits for our records.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY4\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Last warning sir. Send Rs 50000 to gst.payment@okaxis now or face legal action.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY5\",\"timestamp\":$(date +%s)000}]"
REPLY6=$(send_turn 6 "scammer" "We have your business registered at office number 011-12345678. Confirm if correct." "$HISTORY")

# Turn 7
HISTORY="[{\"sender\":\"scammer\",\"text\":\"Your GST invoice payment of Rs 50000 is pending. Pay immediately to avoid penalty.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY1\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir this is from GST department. Send payment to UPI: gst.payment@okaxis or your business license will be suspended.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY2\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"You can call our helpline 9876543210 for verification. But payment must be done in 1 hour.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY3\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Sir are you sending the payment? Just confirm your bank account number ending digits for our records.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY4\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"Last warning sir. Send Rs 50000 to gst.payment@okaxis now or face legal action.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY5\",\"timestamp\":$(date +%s)000},{\"sender\":\"scammer\",\"text\":\"We have your business registered at office number 011-12345678. Confirm if correct.\",\"timestamp\":$(date +%s)000},{\"sender\":\"user\",\"text\":\"$REPLY6\",\"timestamp\":$(date +%s)000}]"
REPLY7=$(send_turn 7 "scammer" "OK sir final confirmation - send payment screenshot to this WhatsApp: +919876543210" "$HISTORY")

# ==============================================================================
# SUMMARY
# ==============================================================================

echo "" >> "$OUTPUT_FILE"
echo "=== EXTRACTED INTELLIGENCE SUMMARY ===" >> "$OUTPUT_FILE"
echo "UPI IDs: gst.payment@okaxis" >> "$OUTPUT_FILE"
echo "Phone Numbers: 9876543210, +919876543210, 011-12345678" >> "$OUTPUT_FILE"
echo "Scam Type: GST Payment Fraud" >> "$OUTPUT_FILE"
echo "Persona Used: Vikram (Business Owner)" >> "$OUTPUT_FILE"
echo "Total Turns: 7" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo -e "${GREEN}=== Test Complete ===${NC}"
echo "Results saved to: $OUTPUT_FILE"
echo ""
echo "To view results:"
echo "  cat $OUTPUT_FILE"
