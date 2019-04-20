"""Defines functions used to collect comments posted on Youtube videos.

"""
import googleapiclient.discovery
import googleapiclient.errors

from youtoxic.app.config import Config


config = Config()


def get_top_level_comments(video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=config.youtube_key)
    threads = list()
    comments = list()
    results = youtube.commentThreads().list(
     part="snippet",
     videoId=video_id,
     textFormat="plainText",
    ).execute()

    #Get the first set of comments
    for item in results["items"]:
        threads.append(item)
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    #Keep getting comments from the following pages
    while ("nextPageToken" in results):
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
        comments.append(text)

    return comments
