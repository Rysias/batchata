from batchata import Batch

def test_simple_batch():
    text_to_batch = ["This is a test", "This is another test", "This is a third test"]
    batcher = Batch(rate_limit=1)
    batches = [batch for batch in batcher.batch(text_to_batch)]
    assert len(batches) == 3
    assert batches[0] == ["This is a test"]

def test_double_rate_limit():
    text_to_batch = ["This is a test", "This is another test", "This is a third test"]
    batcher = Batch(rate_limit=2)
    batches = [batch for batch in batcher.batch(text_to_batch)]
    assert len(batches) == 2
    assert batches[0] == ["This is a test", "This is another test"]

def test_token_limit():
    text_to_batch = ["short word here", "short word here", "short word here", "a very long sentence with many words"]
    batcher = Batch(rate_limit=10, token_limit=9)
    batches = [batch for batch in batcher.batch(text_to_batch)]
    assert len(batches) == 2
    assert batches[1] == ["a very long sentence with many words"]

def test_mix_limts():
    text_to_batch = ["short word here", "short word here", "short word here", "a very long sentence with many words"]
    batcher = Batch(rate_limit=1, token_limit=9)
    batches = [batch for batch in batcher.batch(text_to_batch)]
    assert len(batches) == 4
    assert len(batches[0]) == 1
    assert batches[1] == ["short word here"]
