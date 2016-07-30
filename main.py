"""
Treehouse Video Downloader downloads videos from
the specified Treehouseteam.com video links.

To use it change the username and password and define
the link you would like to download in the links.txt file.

If download fails, the link will be saved in log.txt

"""
import requests

from bs4 import BeautifulSoup
import youtube_dl

USERNAME = 'your_username'
PASSWORD = 'your_password'

for link in open('links.txt'):
    try:
        link = link.strip()
        print(link)
        html = requests.get(link, auth=(USERNAME, PASSWORD))

        soup = BeautifulSoup(html.text, "html.parser")

        # Title
        h1 = soup.h1.contents[0]
        print(h1)

        # Output with the title of the video
        output = u'%(id)s-' + h1 + u'.%(ext)s'

        # Video source link
        tag = soup.video
        videolink = tag.source['src']

        # Youtube-dl options
        options = {
            'outtmpl': output,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([videolink])
    except:
        log = open('log.txt', 'w')
        log.write(link)
        log.close()