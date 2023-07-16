"""Counts tokens for strings or Langchain.messages"""
import tiktoken



def count_tokens(s: str, model="gpt-3.5-turbo") -> int:
    """Counts tokens for strings or Langchain.messages"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(s))
