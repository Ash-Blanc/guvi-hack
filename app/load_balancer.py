"""
Load balancer for API keys.
Rotates through multiple API keys to distribute load and avoid rate limits.
"""
import os
import itertools
from threading import Lock

_lock = Lock()
_key_cycles = {}


def get_balanced_key(env_var: str = "MISTRAL_API_KEY") -> str:
    """
    Get the next API key from a comma-separated list in round-robin fashion.
    
    Args:
        env_var: Environment variable name containing comma-separated keys
    
    Returns:
        The next API key in rotation
    """
    global _key_cycles
    
    with _lock:
        if env_var not in _key_cycles:
            keys_str = os.getenv(env_var, "")
            if not keys_str:
                raise ValueError(f"Environment variable {env_var} is not set")
            
            keys = [k.strip() for k in keys_str.split(",") if k.strip()]
            if not keys:
                raise ValueError(f"No valid keys found in {env_var}")
            
            _key_cycles[env_var] = itertools.cycle(keys)
            print(f"[LOAD BALANCER] Initialized {len(keys)} API keys for {env_var}")
        
        key = next(_key_cycles[env_var])
        # Log key rotation (show only first 8 chars for security)
        print(f"[LOAD BALANCER] Using key: {key[:8]}...")
        return key


def get_mistral_key() -> str:
    """Convenience function for getting balanced Mistral API key."""
    return get_balanced_key("MISTRAL_API_KEY")
