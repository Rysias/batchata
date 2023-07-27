from collections.abc import Generator, Iterable

from .count import count_tokens


class Batch:
    def __init__(
        self,
        rate_limit: int = 1,
        token_limit: int | None = None,
        concurrent_size: int | None = None,
    ):
        """Batch that can account for both rate_limit and token_limit"""
        self.rate_limit = rate_limit
        self.token_limit = token_limit if token_limit is not None else 100_000_000
        self.concurrent_size = concurrent_size
        self.batch = (
            self.batch_concurrent if concurrent_size is not None else self.batch_rate
        )
        pass

    def batch_rate(
        self,
        text_to_batch: Iterable,
    ) -> Generator[Iterable[str], None, None]:
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

    def batch_concurrent(
        self,
        text_to_batch: Iterable,
    ) -> Generator[Iterable[str], None, None]:
        """Batch for concurrent models"""
        batch_size = (
            self.concurrent_size
            if self.concurrent_size is not None
            else self.rate_limit
        )
        batch = []
        for text in text_to_batch:
            batch.append(text)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

    @classmethod
    def from_model(cls: "Batch", model_name: str) -> "Batch":
        """Create a Batch from a model name"""
        if model_name == "gpt-3.5-turbo":
            return cls(rate_limit=3500, token_limit=90_000, concurrent_size=None)
        if model_name == "gpt-4":
            return cls(rate_limit=200, token_limit=40_000, concurrent_size=None)
        if model_name.startswith("claude"):
            return cls(concurrent_size=4)
        raise ValueError(f"Unknown model name: {model_name}")
