import requests
from bs4 import BeautifulSoup

# url = 'https://www.youtube.com/watch?v=C4hZsLMGR9M'

KEY = "AIzaSyCbIdhM3sBth8tCJ7Nln9XQ19iipJSM5PM"
CHANNEL_ID = "UCFmL725KKPx2URVPvH3Gp8w"
# CHANNEL_ID = "OneDirectionVEVO"
CHANNEL_CONTENT_REQ = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={}&key={}"
VIDEO_URLS_REQ = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}"

def get_resource(url, id, key):
    resource = url.format(id, key)

    response = requests.get(resource)
    if response.status_code == 200:
        print(".", "url:", url[url.find("v3/")+3:],  "status:", response.status_code, "size:", len(response.content)/1000, "kb")
    else:
        print("!", "url:", url[url.find("v3/")+3:],  "status:", response.status_code, "size:", len(response.content)/1000, "kb")
    return response

if __name__ == "__main__":
    channel_content_resp = get_resource(CHANNEL_CONTENT_REQ, CHANNEL_ID, KEY).json()
    uploads_playlist_id = channel_content_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    video_urls = get_resource(VIDEO_URLS_REQ, uploads_playlist_id, KEY).json()

    # print(uploads_playlist_id)
    print(video_urls)



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


