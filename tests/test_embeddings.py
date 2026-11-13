
from src.embeddings import get_embedding_model


def test_embedding_generation():

    embedding_model = get_embedding_model()

    text = "Machine learning is a branch of artificial intelligence."

    vector = embedding_model.embed_query(text)

    assert len(vector) == 384

    assert all(isinstance(value, float) for value in vector)

    print("Embedding generation test passed!")
    print("Vector dimensions:", len(vector))
