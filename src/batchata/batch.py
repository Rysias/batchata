from collections.abc import Generator, Iterable

from .count import count_tokens


class Batch:
    def __init__(self, rate_limit: int = 1, token_limit: int | None = None):
        """Batch that can account for both rate_limit and token_limit"""
        self.rate_limit = rate_limit
        self.token_limit = token_limit if token_limit is not None else 100_000_000
        pass

    def batch(self, text_to_batch: Iterable) -> Generator[Iterable[str], None, None]:
        """Batch while accounting for both rate_limit and token_limit"""
        current_tokens = 0
        rate_count = 0
        batch = []

        for text in text_to_batch:
            tokens = count_tokens(text)
            token_check = current_tokens + tokens > self.token_limit
            rate_check = rate_count % self.rate_limit == 0
            if len(batch) == 0 or token_check or rate_check:
                if batch:
                    yield batch
                batch = [text]
                current_tokens = tokens
            else:
                batch.append(text)
                current_tokens += tokens
            rate_count += 1

        if batch:
            yield batch
