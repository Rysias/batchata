from typing import Sequence, Generator

from .count import count_tokens

class Batch:
    def __init__(self, rate_limit: int = 1, token_limit: int | None = None):
        self.rate_limit = rate_limit
        self.token_limit = token_limit if token_limit is not None else 100_000_000
        pass


    def batch(self, text_to_batch) -> Generator[Sequence[str], None, None]:
        """Batch while accounting for both rate_limit and token_limit"""
        current_tokens = 0
        rate_count = 0
        batch = []
        for text in text_to_batch:
            if len(batch) == 0:
                batch.append(text)
                current_tokens = count_tokens(text)
                rate_count = 1
            elif current_tokens + count_tokens(text) > self.token_limit:
                yield batch
                batch = [text]
                current_tokens = count_tokens(text)
                rate_count = 1
            elif rate_count == self.rate_limit:
                yield batch
                batch = [text]
                current_tokens = count_tokens(text)
                rate_count = 1
            else:
                batch.append(text)
                current_tokens += count_tokens(text)
                rate_count += 1
        if batch:
            yield batch

