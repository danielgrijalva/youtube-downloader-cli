from youtube_dl import YoutubeDL
import subprocess
from pprint import pprint


class Download:
    def __init__(self, ydl):
        self.ydl = ydl
        self.url, self.start_from, self.duration = self.setup()
        self.video_info = self.extract_video_info()
        
    def setup(self):
        url = input('URL: ')

        if 't=' in url:
            start_from = url.split('t=')[1]
        else:
            start = input('START FROM (HH:MM:SS): ')
            start_from = self.string_to_seconds(start)

        duration = input('DURATION: ')

        return url, start_from, duration

    def string_to_seconds(self, string):
        h, m, s = string.split(':')

        return int(h) * 3600 + int(m) * 60 + int(s)

    def extract_video_info(self):
        return self.ydl.extract_info(self.url, download=False)

    def obtain_formats(self):
        return self.video_info['requested_formats']

    def get_video_title(self):
        title = list(self.video_info['title'])
        prohibited_chars = '\/:*?"<>|'
        for char in title:
            if char in prohibited_chars:
                del title[title.index(char)]
        
        self.title = ''.join(title)
        self.filename = f'{self.title} @ {self.start_from}.mp4'

    def get_video_audio_url(self):
        formats = self.obtain_formats()
        pprint(formats)
        self.video_url = formats[0]['url']
        self.audio_url = formats[1]['url']

    def download(self):
        ffmpeg_command = [ 'ffmpeg',
            '-ss', str(self.start_from), '-i', self.video_url,
            '-ss', str(self.start_from), '-i', self.audio_url,
            '-t', self.duration, '-c:v', 'copy', '-c:a', 'copy', self.filename
        ]

        try:
            subprocess.run(ffmpeg_command)
            print('FINISHED: {}'.format(self.filename))
        except Exception as e:
            print(e)

        
ydl = YoutubeDL({'quiet': True})
d = Download(ydl)
d.extract_video_info()
d.get_video_title()
d.get_video_audio_url()
d.download()
