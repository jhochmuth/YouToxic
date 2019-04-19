from tests.unit.client import client  # noqa:

from youtoxic.app.services.pipeline import Pipeline


def test_get_text_classifications(client):  # noqa:
    """Unittest for basic text classification."""
    pipeline = Pipeline()
    pred, judgement = pipeline.predict_toxicity_ulm('blah blah')
    assert 0 <= pred <= 1
