try:
    from ytmusicapi import YTMusic
except ImportError:
    import os, sys
    os.system(f"{sys.executable} -m pip install ytmusicapi")
    import ytmusicapi

import time
import concurrent.futures # import multi threading library
import os
import json
from datetime import date

ytmusic = YTMusic()

def get_song_url(query):
    print(f"Searching Query: {query}")
    search_result = ytmusic.search(query, "songs", None, 1)
    song_id = search_result[0]["videoId"]
    print(f"Found Song ID: {song_id} For Song {query}")
    song_urls.append(f"https://music.youtube.com/watch?v={song_id}")

song_urls = []

unformatted = json.loads(input("Paste in the list of songs and artists here: "))
song_list = []

for song in unformatted:
    song_list.append(" ".join(song))

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor: # Searches Song on Youtube Music
    executor.map(get_song_url, song_list)

with open(f"{date.today()} - song_url_list.txt", "wt") as song_url_list: # Writes Result to File
    song_url_list.write("\n".join(song_urls))

# Customize The Download Command, ex. --audio-format, --audio-quality, and the metadata settings.
base_download_command = """yt-dlp -fbestaudio --extract-audio --audio-format mp3 --audio-quality 9 --embed-thumbnail --add-metadata -o "%(title)s - %(artist)s.%(ext)s" --playlist-items 1 --ppa "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\\\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\\\"\""""


def download_song(url):
    time.sleep(2)
    # executing yt-dlp commands
    os.system(f"{base_download_command} \"{url}\"")

# max_worker will determine how many songs will be downloaded at the same time
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(download_song, song_urls)
    # this will map the elements inside song_urls to the function download_songs
