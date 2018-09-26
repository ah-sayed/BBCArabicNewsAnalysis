from apiclient.discovery import build
from apiclient.errors import HttpError
import csv
import unidecode

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)


    search_response = youtube.search().list(
        q=q,
        type="video",
        pageToken=token,
        order = order,
        channelId = 'UCelk6aHijZq-GJBBB9YpReA',
        part="id,snippet",
        maxResults=max_results,
        location=location,
        locationRadius=location_radius,
        #videoDuration="any"

    ).execute()
    
    # create a CSV output for video list    
    csvFile = open('videos53.csv','w+')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["title","videoId","viewCount","likeCount","dislikeCount","commentCount","videoDuration", "Date"])
    
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            #videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  # Dongho 08/10/16
            videoId = search_result["id"]["videoId"]
            
            video_response = youtube.videos().list(
                id=videoId,
                part='statistics, contentDetails, status, snippet').execute()
                
            for video_result in video_response.get("items",[]):
                viewCount = video_result["statistics"]["viewCount"]
                if "publishedAt" not in video_result["snippet"]:
                    Date = '0000-00-00'
                else:
                    Date = video_result["snippet"]["publishedAt"]
                if "duration" not in video_result["contentDetails"]:
                    videoDuration = 0
                else:
                    videoDuration = video_result["contentDetails"]["duration"]
                if 'likeCount' not in video_result["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_result["statistics"]["likeCount"]
                if 'dislikeCount' not in video_result["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_result["statistics"]["dislikeCount"]
                if 'commentCount' not in video_result["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_result["statistics"]["commentCount"]
                
                    
            csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,videoDuration, Date])

    csvFile.close()


def geo_query(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(
        id=video_id,
        part='snippet, recordingDetails, statistics'

    ).execute()

    return video_response

#key_words = ['BBCArabicNews', 'BBC News عربي', 'BBC Arabic']
youtube_search('BBCArabicNews')
