from tests.unit.client import client  # noqa:

from youtoxic.app.services.pipeline import Pipeline


text = "blah blah"


def test_get_text_classifications(client):  # noqa:
    """Unittest for basic text classification."""
    pipeline = Pipeline()
    pred, judgement = pipeline.predict_toxicity_ulm(text)
    assert 0 <= pred <= 1
