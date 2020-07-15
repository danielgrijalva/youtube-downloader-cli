from download import Download
from youtube_dl import YoutubeDL
from alive_progress import alive_bar


if __name__ == '__main__':
    options = {
        'quiet': True,
        'restrictfilenames': True,
        'format': 'bestvideo+bestaudio'
    }
    ydl = YoutubeDL(options)
    d = Download(ydl)
    with alive_bar(spinner='dots_reverse', unknown='message_scrolling') as bar:
        d.extract_video_info()
        # d.get_video_title()
        d.get_video_audio_url()
        filename = d.download()
