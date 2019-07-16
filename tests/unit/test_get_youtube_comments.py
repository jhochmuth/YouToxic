from tests.unit.client import client  # noqa:

from youtoxic.app.services.youtube_comment_dumper import get_top_level_comments


youtube_url = "https://www.youtube.com/watch?v=NYl_UcGSQeU"


def test_get_youtube_comments(client):  # noqa:
    """Unittest for collecting youtube comments."""
    comments = get_top_level_comments(youtube_url)
    assert(comments is not None and len(comments[0] == len(comments[1] == len(comments[2]))))
