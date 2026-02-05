import os

# Central Model Configuration
# Change this ONE value to update all agents
DEFAULT_MODEL_ID = "mistral-small-latest"

# Specific Role Overrides (currently mapped to default)
# You can change these individually if you want different models for different roles
TEAM_LEADER_MODEL_ID = DEFAULT_MODEL_ID
SCAM_DETECTOR_MODEL_ID = DEFAULT_MODEL_ID
HONEYPOT_MODEL_ID = DEFAULT_MODEL_ID
SIMULATOR_MODEL_ID = DEFAULT_MODEL_ID
