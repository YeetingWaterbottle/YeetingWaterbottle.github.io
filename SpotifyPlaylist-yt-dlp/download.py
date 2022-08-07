import time
import concurrent.futures # import multi threading library
import os

song_urls = []

song_list = input("Enter Generated 'songs.txt' Location: ")

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

# Customize The Download Command, ex. --audio-format, --audio-quality, and the metadata settings.
base_download_command = """yt-dlp -fbestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata -o "%(title)s - %(artist)s.%(ext)s" --playlist-items 1 --ppa "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\\\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\\\"\""""
# For Detailed Explinations, go to https://github.com/yt-dlp/yt-dlp
# -fbestaudio           download song with the best audio
# --extract-audio       extract the audio from the video (duh)
# --audio-format        encode audio into different file formats (mp3, flac, wav, etc.)
# --audio-quality       the number after this parameter will determine the audio quality. 0 being the best, 10 being the worst.
# --embed-thumbnail     embed thumbnail to audio file (this does not work with file types like wav)
# --add-metadata        adds metadata like song name, artist name, album name, etc.
# -o                    output template
# --playlist-items      this will limit how many songs will download, in this script it will only download the top result
# --ppa "Emb...         this will crop the album cover into a square one


def download_song(url):
    # executing yt-dlp commands
    os.system(f"{base_download_command} \"{url}\"")
    time.sleep(2)

# max_worker will determine how many songs will be downloaded at the same time
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(download_song, song_urls)
    # this will map the elements inside song_urls to the function download_songs