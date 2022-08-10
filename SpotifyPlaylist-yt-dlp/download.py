try:  # try to import ytmusicapi library, if it does not exist install for user.
    from ytmusicapi import YTMusic
except ImportError:
    ask = input(
        "The ytmusicapi Library Does Not Exist, Install Automatically? (y/n) ")
    while ask.lower() not in ["y", "n"]:
        print("Input Was Not Valid")
        ask = input(
            "The ytmusicapi Library Does Not Exist, Install Automatically? (y/n) ")
    if ask == "y":
        import os
        import sys
        os.system(f"{sys.executable} -m pip install ytmusicapi")
        from ytmusicapi import YTMusic
    if ask == "n":
        input("Press Enter To Exit.")
        quit()

import time
import concurrent.futures  # multi threading library
import os
import json
from datetime import date
from difflib import SequenceMatcher


ytmusic = YTMusic()

def detect_wrong_song(original_search, result):
    if SequenceMatcher(None, original_search.lower(), result.lower()).ratio() < 0.4:
        with open("This Song Might Be Wrong.txt", "a+") as warning_file:
            warning_file.write(
                f"The Search \"{original_search}\" Might Not Have Matched Your Desired Result, Check the Downloaded Song \"{result}\".\n")
            print("Check \"This Song Might Be Wrong.txt\"")

def get_song_url(query):
    print(f"Searching Query: {query}")
    search_result = ytmusic.search(query, "songs", None, 1)[0]
    song_id = search_result["videoId"]
    song_title = search_result["title"]
    detect_wrong_song(query, song_title)
    print(f"Found Song ID: {song_id} For Song \"{song_title}\" Searching: \"{query}\"")
    song_urls.append(f"https://music.youtube.com/watch?v={song_id}")


def download_song(url):
    time.sleep(2)
    # executing yt-dlp commands
    os.system(f"{base_download_command} \"{url}\"")


song_urls = []

# Customize The Download Command, ex. --audio-format, --audio-quality, and the metadata settings.
base_download_command = """yt-dlp -fbestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata -o "%(title)s - %(artist)s.%(ext)s" --playlist-items 1 --ppa "EmbedThumbnail+ffmpeg_o:-c:v mjpeg -vf crop=\\\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\\\"\""""

option = input(
    "What Do You Want to Do?\n(1) Download Spotify Playlist.\n(2) Search and Download Single Song.\n(3) Download Song With Youtube Link\nChoice: ")

while option not in ["1", "2", "3"]:
    print("Input Was Not Valid")
    option = input(
        "What Do You Want to Do? (1) Download Spotify Playlist. (2) Search and Download Single Song.\nChoice: ")

if option == "1":
    unformatted = json.loads(
        input("Paste in the list of songs and artists here: "))
    song_list = []

    for song in unformatted:
        song_list.append(" ".join(song))

    # Searches Song on Youtube Music
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(get_song_url, song_list)

    with open(f"{date.today()} - song_url_list.txt", "wt") as song_url_list:  # Writes Result to File
        song_url_list.write("\n".join(song_urls))

    # max_worker will determine how many songs will be downloaded at the same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_song, song_urls)
        # this will map the elements inside song_urls to the function download_songs

if option == "2":
    search_term = input(
        "What Song Do You Want to Download? (Add Artist Names to Make Result More Accurate): ")
    get_song_url(search_term)
    download_song(song_urls[0])

if option == "3":
    link = input("Input Song Url, ex. (music.)youtube.com/watch?v=eEYO0rKL6vk | https://youtu.be/eEYO0rKL6vk\nLink: ")
    download_song(link)



input("Songs Finished Downloading, Press Enter to Exit Program.")