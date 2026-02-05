from agno.models.mistral import MistralChat
from agno.models.openai import OpenAIChat
from .config import ENABLE_FALLBACK
import os

class ReliableMistral(MistralChat):
    """
    A specific wrapper for MistralChat that catches 429/RateLimit errors
    and falls back to Pollinations.ai (OpenAI compatible).
    """
    
    def invoke(self, *args, **kwargs):
        try:
            return super().invoke(*args, **kwargs)
        except Exception as e:
            if self._should_fallback(e):
                print(f"[RELIABLE_LLM] ⚠️ Primary Mistral model failed with {e}. Switching to Pollinations.ai fallback...")
                return self._get_fallback_model().invoke(*args, **kwargs)
            raise e

    def response(self, *args, **kwargs):
        try:
            return super().response(*args, **kwargs)
        except Exception as e:
            if self._should_fallback(e):
                print(f"[RELIABLE_LLM] ⚠️ Primary Mistral model failed with {e}. Switching to Pollinations.ai fallback...")
                return self._get_fallback_model().response(*args, **kwargs)
            raise e

    def _should_fallback(self, error: Exception) -> bool:
        """Check if fallback should be triggered based on config and error type."""
        if not ENABLE_FALLBACK:
            return False
            
        error_msg = str(error).lower()
        # Check for common rate limit or capacity indicators
        if "429" in error_msg:
            return True
        if "capacity exceeded" in error_msg:
            return True
        if "rate limit" in error_msg:
            return True
        return False

    def _get_fallback_model(self):
        """Returns the configured fallback model (Pollinations.ai)."""
        # Pollinations.ai text generation endpoint
        return OpenAIChat(
            id="nova-fast",  # Using nova-fast as requested
            base_url="https://text.pollinations.ai/openai",
            api_key="dummy",  # Pollinations doesn't strictly enforce key check for free tier
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

def get_model(model_id: str, api_key: str = None, **kwargs):
    """
    Factory function to get a reliable model instance.
    """
    if api_key is None:
        api_key = os.getenv("MISTRAL_API_KEY")
        
    return ReliableMistral(
        id=model_id,
        api_key=api_key,
        **kwargs
    )
