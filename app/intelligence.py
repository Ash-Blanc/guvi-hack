import re
from typing import List
from .models import ExtractedIntelligence

# Regex patterns for extraction
UPI_PATTERN = r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}'
PHONE_PATTERN = r'(?:\+91|0)?[6-9]\d{9}'
BANK_ACC_PATTERN = r'\b\d{9,18}\b'
URL_PATTERN = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

# Suspicious keywords
SCAM_KEYWORDS = [
    "blocked", "verify", "suspended", "urgent", "kyc", "update", "lottery",
    "win", "congratulations", "bank", "password", "otp", "pin"
]

def extract_intelligence(text: str) -> ExtractedIntelligence:
    """
    Analyzes the message text to extract specific intelligence like UPI IDs, phone numbers, bank accounts, and phishing links.
    Use this to confirm specific structured data from the scam start.
    """
    upi_ids = re.findall(UPI_PATTERN, text)
    phone_numbers = re.findall(PHONE_PATTERN, text)
    bank_accounts = re.findall(BANK_ACC_PATTERN, text)
    urls = re.findall(URL_PATTERN, text)
    
    found_keywords = [kw for kw in SCAM_KEYWORDS if kw in text.lower()]
    
    return ExtractedIntelligence(
        bankAccounts=list(set(bank_accounts)),
        upiIds=list(set(upi_ids)),
        phishingLinks=list(set(urls)),
        phoneNumbers=list(set(phone_numbers)),
        suspiciousKeywords=list(set(found_keywords))
    )

def is_scam(text: str, extracted: ExtractedIntelligence) -> bool:
    # A message is likely a scam if it contains phishing links OR suspicious keywords + bank/UPI/phone triggers
    if extracted.phishingLinks:
        return True
    
    has_identifiers = extracted.bankAccounts or extracted.upiIds or extracted.phoneNumbers
    if extracted.suspiciousKeywords and has_identifiers:
        return True
    
    # Check for "verify" + "blocked" style urgency
    text_lower = text.lower()
    if ("verify" in text_lower or "update" in text_lower) and "block" in text_lower:
        return True
        
    return False
