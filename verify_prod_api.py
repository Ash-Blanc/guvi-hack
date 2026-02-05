import requests
import json
import time
import uuid

# Configuration
BASE_URL = "https://honey-pot-api-production.up.railway.app"
API_KEY = "3INM.bT.0ZgI6ORYVUDTuGKfg743erlt"
ENDPOINT = f"{BASE_URL}/analyze"

# Session Setup
SESSION_ID = str(uuid.uuid4())
print(f"Starting Test Session: {SESSION_ID}")

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

conversation_history = []

def send_message(text, sender="scammer"):
    global conversation_history
    
    timestamp = int(time.time() * 1000)
    current_message = {
        "sender": sender,
        "text": text,
        "timestamp": timestamp
    }
    
    payload = {
        "sessionId": SESSION_ID,
        "message": current_message,
        "conversationHistory": conversation_history,
        "metadata": {
            "channel": "terminal_test",
            "language": "en",
            "locale": "IN"
        }
    }
    
    print(f"\n--- Sending Message ---\n'{text}'")
    start_time = time.time()
    
    try:
        response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=30)
        end_time = time.time()
        duration = round((end_time - start_time), 2)
        
        print(f"Status Code: {response.status_code}")
        print(f"Latency: {duration} seconds")
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("reply", "NO_REPLY_FOUND")
            print(f"Agent Reply: {reply}")
            
            # Update history
            conversation_history.append(current_message)
            conversation_history.append({
                "sender": "user", # The agent acts as the 'user' (victim)
                "text": reply,
                "timestamp": int(time.time() * 1000)
            })
            return True
        else:
            print(f"Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Request Failed: {e}")
        return False

# --- Scenario Execution ---

# 1. Start with a classic scam message
print("\n[Step 1] Initial Scam Message")
if not send_message("URGENT: Your SBI account will be blocked today due to KYC update. Click link immediately: http://bit.ly/sbi-kyc-update"):
    print("Stopping test due to error.")
    exit()

# 2. Wait a bit (simulate human typing speed)
time.sleep(2)

# 3. Follow up pressing for urgency
print("\n[Step 2] Follow-up Urgency")
if not send_message("Why are you not responding? Send the OTP or your money is lost."):
    exit()

# 4. Ask for banking details to trigger high-value intel logic
print("\n[Step 3] Phishing for Details")
if not send_message("Just send your card number and CVV to this number +919876543210 and I will unblock it."):
    exit()

print("\n--- Test Complete ---")
