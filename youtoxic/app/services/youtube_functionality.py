"""Defines functions used to collect comments posted on Youtube videos.

"""
import googleapiclient.discovery as discovery
import googleapiclient.errors as errors

from youtoxic.app.config import Config


config = Config()


def get_top_level_comments(video_id):
    """"Returns a list of all top-level comments posted on a youtube video.

    Parameters
    ----------
    video_id
        Comments will be retrieved from the youtube video that has this id.

    Returns
    -------
    list of str or None
        The list containing the top-level comments.
        It will be empty if there were no comments.
        None will be returned if no video was found with the specified id.

    """
    youtube = discovery.build("youtube", "v3", developerKey=config.youtube_key)
    threads, comments, authors, times = list(), list(), list(), list()

    try:
        results = youtube.commentThreads().list(part="snippet",
                                                videoId=video_id,
                                                textFormat="plainText").execute()
    except errors.HttpError:
        return None

    # Get the first set of comments

    for item in results["items"]:
        threads.append(item)
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        author = comment["snippet"]["authorDisplayName"]
        time = comment["snippet"]["publishedAt"]
        comments.append(text)
        authors.append(author)
        times.append(time)

    # Keep getting comments from the following pages
    while "nextPageToken" in results:
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=results["nextPageToken"],
            textFormat="plainText",
        ).execute()

        for item in results["items"]:
            threads.append(item)
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            author = comment["snippet"]["authorDisplayName"]
            time = comment["snippet"]["publishedAt"]
            comments.append(text)
            authors.append(author)
            times.append(time)

    return comments, authors, times
