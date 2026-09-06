import math

import pytest

from soundsplit_knowledge.embeddings import HttpEmbedder, validate_vectors
from soundsplit_knowledge.models import DIMENSIONS, KnowledgeError


def test_remote_embedding_worker_is_rejected():
    with pytest.raises(KnowledgeError, match="loopback"):
        HttpEmbedder("https://example.com")


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_invalid_vector_values_are_rejected(bad):
    vector = [0.0] * DIMENSIONS
    vector[0] = bad
    with pytest.raises(KnowledgeError, match="invalid"):
        validate_vectors([vector], 1)


def test_nonzero_finite_vector_is_accepted():
    vector = [0.0] * DIMENSIONS
    vector[0] = 1.0
    assert validate_vectors([vector], 1) == [vector]
    assert math.isfinite(vector[0])
