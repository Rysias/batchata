import pytest
from batchata import Batch


def test_simple_batch():
    text_to_batch = ["This is a test", "This is another test", "This is a third test"]
    batcher = Batch(rate_limit=1)
    batches = list(batcher.batch(text_to_batch))
    assert len(batches) == 3
    assert batches[0] == ["This is a test"]


def test_double_rate_limit():
    text_to_batch = ["This is a test", "This is another test", "This is a third test"]
    batcher = Batch(rate_limit=2)
    batches = list(batcher.batch(text_to_batch))
    assert len(batches) == 2
    assert batches[0] == ["This is a test", "This is another test"]


def test_token_limit():
    text_to_batch = [
        "short word here",
        "short word here",
        "short word here",
        "a very long sentence with many words",
    ]
    batcher = Batch(rate_limit=10, token_limit=9)
    batches = list(batcher.batch(text_to_batch))
    assert len(batches) == 2
    assert batches[1] == ["a very long sentence with many words"]


def test_mix_limts():
    text_to_batch = [
        "short word here",
        "short word here",
        "short word here",
        "a very long sentence with many words",
    ]
    batcher = Batch(rate_limit=1, token_limit=9)
    batches = list(batcher.batch(text_to_batch))
    assert len(batches) == 4
    assert len(batches[0]) == 1
    assert batches[1] == ["short word here"]


def test_concurrent():
    text_to_batch = ["This is a test", "This is another test", "This is a third test"]
    batcher = Batch(rate_limit=1, concurrent_size=2)
    batches = list(batcher.batch_concurrent(text_to_batch))
    assert len(batches) == 2
    assert len(batches[0]) == 2
    assert batches[1] == ["This is a third test"]


def test_from_gpt():
    batcher = Batch.from_model("gpt-3.5-turbo")
    assert batcher.rate_limit == 3500
    assert batcher.token_limit == 90_000


def test_from_unknown():
    with pytest.raises(ValueError, match=r"Unknown model name: .*"):
        Batch.from_model("unknown-model")


def test_from_claude():
    to_batch = ["a", "b", "c", "d", "e", "f", "g", "h"]
    batcher = Batch.from_model("claude")
    batches = list(batcher.batch(to_batch))
    assert batcher.concurrent_size == 4
    assert len(batches) == 2
