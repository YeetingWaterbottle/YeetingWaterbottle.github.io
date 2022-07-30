import time
import concurrent.futures
import os

song_urls = []

song_list = input("Enter Generated Song Url Location: ")

try:
    with open(song_list) as f:
        songs = f.read().splitlines()
        for song in songs:
            if song.startswith("#"):
                continue
            
            song_urls.append(song)

except FileNotFoundError:
    print("Error: File Not Found.")
    input("Press Enter to Close.")
    quit()


base_download_command = """yt-dlp -fbestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata -o "%(title)s - %(artist)s.%(ext)s" --playlist-items 1 --ppa "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\\\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\\\"\" --sponsorblock-remove music_offtopic"""

def download_song(url):
    os.system(f"{base_download_command} \"{url}\"")
    time.sleep(2)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(download_song, song_urls)