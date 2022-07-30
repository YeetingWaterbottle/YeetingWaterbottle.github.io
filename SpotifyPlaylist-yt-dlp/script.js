function download(filename, text) {
    let element = document.createElement("a");
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(text));
    element.setAttribute("download", filename);

    element.style.display = "none";
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function load_songs(songs) {
    let result = "";
    let song_num = 1;
    // important, music.youtube.com will not download if the result is music video
    // youtube.com will download the first result which could be a music video
    // let base_url = "https://music.youtube.com/search?q=";
    let base_url = "https://youtube.com/search?search_query=";
    for (let song_info of JSON.parse(songs)) {
        // song_info[0] -> Song Name
        // song_info[1] -> Artists
        result += `#${song_num}. ${song_info[0]} - ${song_info[1]}` + "\n";
        // Bitch, Don't Kill My Vibe description:"Kendrick Lamar Provided to YouTube"
        result += base_url + encodeURIComponent(`${song_info[0]} description:"${song_info[1]} Provided to YouTube"`) + "\n";
        song_num += 1;
    }

    return result;
}

function get_song() {
    download("songs.txt", load_songs(document.getElementById("song_info").value));
    document.getElementById("instructions").style.display = "block";

    document.getElementById("yt-dlp_command").innerHTML = `yt-dlp -a songs.txt -fbestaudio --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata -o "%(title)s - %(artist)s.%(ext)s" --playlist-items 1 --ppa "ffmpeg: -c:v mjpeg -vf crop=\\\"'if(gt(ih,iw),iw,ih)':'if(gt(iw,ih),ih,iw)'\\\""`
    document.getElementById("yt-dlp_command").style.display = "block";
}
