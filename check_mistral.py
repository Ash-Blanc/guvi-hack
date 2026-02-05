try:
    from agno.models.mistral import MistralChat
    print("MistralChat available")
except ImportError as e:
    print(f"ImportError: {e}")
