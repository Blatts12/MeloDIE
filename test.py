import youtube_dl

yt_link = "https://www.youtube.com/watch?v=HLetFEpgPgY"

_ydl_opts_info = {
    "format": "bestaudio/best",
    # "forceurl": True,
    "dump_single_json": True,
}

info = {}

with youtube_dl.YoutubeDL(_ydl_opts_info) as ydl:
    try:
        info = ydl.extract_info(yt_link, download=False)
        info["error"] = False
    except Exception as e:
        info = {"error": True, "desc": e}

print(info["url"])