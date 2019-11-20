import requests
from bs4 import BeautifulSoup
import pprint

# API KEY
API_KEY = "AIzaSyCbIdhM3sBth8tCJ7Nln9XQ19iipJSM5PM"

# CHANNEL IDS
CHANNEL_IDS = ["UCFmL725KKPx2URVPvH3Gp8w"]

# PARTS
CD = "contentDetails"
SNIP = "snippet"

# PARAMS
PL_ID = "playlistId"
ID = "id"
PT = "pageToken"

# REQUEST URLS
CHANNEL_REQ = f"https://www.googleapis.com/youtube/v3/channels?part={CD}&{ID}={}&key={API_KEY}"
PLAYLIST_ITEMS_REQ = f"https://www.googleapis.com/youtube/v3/playlistItems?part={CD}&{PL_ID}={}&{PT}={}&key={API_KEY}"
VIDEO_REQ = f"https://www.googleapis.com/youtube/v3/videos?part={SNIP}&{ID}={}&key={API_KEY}"


def get_resource(url, *params):
    if len(params) == 2:
        id, key = params
        resource = url.format(id, key)
    if len(params) == 3:
        id, page_token, key = params
        resource = url.format(id, page_token, key)

    response = requests.get(resource)

    if response.status_code == 200:
        print("\u001b[32m", \
              ".", \
              "url:", url[url.find("v3/")+3:url.find("&key")], \
              "status:", response.status_code, \
              "size:", len(response.content)/1000, "kb" \
              "\u001b[0m")
    else:
        print("\u001b[31m", \
              "!", \
              "url:", url[url.find("v3/")+3:url.find("&key")], \
              "status:", response.status_code, \
              "size:", len(response.content)/1000, "kb" \
              "\u001b[0m")

    return response

def recursive_lookup(key, nested_dict):
    if isinstance(nested_dict, list):
        for i in nested_dict:
            for x in recursive_lookup(key, i):
               yield x
    elif isinstance(nested_dict, dict):
        if key in nested_dict:
            yield nested_dict[key]
        for j in nested_dict.values():
            for x in recursive_lookup(key, j):
                yield x

class YoutubeVideo():
    def __init__(self):
        self.date = None # publishedAt
        self.title = "" # title
        self.description = "" # description
        self.tags = []
        self.thumbnail_url = "" # url
        self.video_url = "" # videoId


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(compact=True)

    for channel_id in CHANNEL_IDS:

        channel_content = get_resource(CHANNEL_REQ, channel_id, API_KEY).json()

        uploads_id = next(recursive_lookup('uploads', channel_content), None)
        
        video_urls = []
        page_token = ""

        while(page_token is not None):
            playlist_content = get_resource(PLAYLIST_CONTENT_REQ, uploads_id, page_token, API_KEY).json()

            video_urls += list(recursive_lookup('videoId', playlist_content))
            
            page_token = next(recursive_lookup('nextPageToken', playlist_content), None)

        # print(video_urls)

        for url in video_urls:
            video = get_resource

        


    # response = requests.get(api_req)
    # if response.status_code == 200:
    #     print(".", "url:", url,  "status:", response.status_code, "size:", len(response.content)/1000, "kb")
    # else:
    #     print("!", "url:", url,  "status:", response.status_code, "size:", len(response.content)/1000, "kb")

    # print(response.text)

    # soup = BeautifulSoup(response.text, "html.parser")
    # tags = soup.find_all("meta", property="og:video:tag")
    # for tag in tags:
    #     print(tag.get("content"))


