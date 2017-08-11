"""
Treehouse Video Downloader downloads videos from
the specified Treehouseteam.com courses and workshops.

To use it change the username and password and define
the course/workshop you would like to download in the
links.txt file.

If you would like to download the **subtitles** of the
videos set `SUBTITLES = True`. They are not downloaded
by default.

If download fails, the link will be saved in log.txt
"""

import requests
import os
import re

from bs4 import BeautifulSoup
import youtube_dl

USERNAME = 'your_username'
PASSWORD = 'your_password'

# Download subtitles of the videos
SUBTITLES = False
HOME_DIR = os.getcwd()


def move_to_course_directory(title):
    """Check if current directory is home directory. If not, change to it.
    Make a course directory and move to it.
    If course directory already exists, just move to it.
    If everything fails break the program.
    """

    # Move to home directory if we are somewhere else (e.g. course subdir)
    if os.getcwd() != HOME_DIR:
        os.chdir(HOME_DIR)
    try:
        # Make a directory with course name
        os.mkdir(title)
        os.chdir(title)
    except FileExistsError:
        # Position yourself in course directory
        os.chdir(title)
    except:
        print('Could not create subdirectory for the course: {}'.format(title))


def getID(link):
    """Go to the web page with the video and extract its ID
    """
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "html.parser")
    for id in soup.select('meta[property="og:url"]'):
        parts = id['content'].split('/')
        id = parts[-1]
        return id


def getSubtitles(id, name):
    """ Download and rename subtitle file to match the downloaded videos.
    Subtitle is located at https://teamtreehouse.com/videos/{id}}/captions
    """
    subtitlesLink = 'https://teamtreehouse.com/videos/{}/captions'.format(id)
    response = requests.get(subtitlesLink)
    if response.status_code == 200:
        contentDisposition = response.headers['Content-Disposition']
        parts = contentDisposition.split('"')
        title = '{}-{}'.format(name, parts[-2])
        content = response.text
        with open(title, 'w') as f:
            f.write(content)
        return 0


def getLinksCourse(link):
    """ Get the content of stages and extract the links to videos
    """
    # Prepare URL with stages
    linkToStages = '{}{}'.format(link, '/stages')
    html = requests.get(linkToStages)
    soup = BeautifulSoup(html.text, "html.parser")

    # Find all urls of the videos (ignore reviews and questions)
    videos = []
    for a in soup.select('a[href^="/library/"]'):
        if (a.select('.video-22-icon')):  # if video icon is there
            videoLink = '{}{}'.format('https://teamtreehouse.com', a['href'])
            videos.append(videoLink)
    print(videos)
    return videos


def getLinksWorkshop(link):
    """ Get the links to videos from workshop page
    """
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "html.parser")

    # Find all urls of the videos
    videos = []
    for a in soup.select('li.workshop-video a[href^="/library/"]'):
        vidLink = '{}{}'.format('https://teamtreehouse.com', a['href'])
        videos.append(vidLink)
    return videos


def getLinkWorkshop(link):
    """ Get the link to video from workshop page - only one video workshop
    """
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "html.parser")

    # Find all urls of the videos
    videos = []
    for a in soup.select('a#workshop-hero'):
        vidLink = '{}{}'.format('https://teamtreehouse.com', a['href'])
        videos.append(vidLink)
    return videos


for link in open('links.txt'):
    try:
        link = link.strip()
        print('Downloading: {}'.format(link))

        videos = getLinksWorkshop(link) or getLinkWorkshop(link) or getLinksCourse(
            link)

        # Generate folder name and move to it
        parts = link.split('/')
        title = parts[-1]
        move_to_course_directory(title)

        for video in videos:

            html = requests.get(video, auth=(USERNAME, PASSWORD))
            soup = BeautifulSoup(html.text, "html.parser")

            # Extract title for filename
            h1 = soup.h1.contents[0]

            # Output with the title of the video
            output = u'%(id)s-' + h1 + u'.%(ext)s'

            # Video source link
            tag = soup.video
            videolink = tag.source['src']

            # Youtube-dl options
            options = {
                'outtmpl': output
                # ,'verbose': True
            }

            with youtube_dl.YoutubeDL(options) as ydl:

                ydl.download([videolink])

                if (SUBTITLES):
                    ID = getID(video)
                    info = ydl.extract_info(videolink, download=False)
                    name = info.get('title', None)
                    subs = getSubtitles(ID, name)

    except:
        os.chdir(HOME_DIR)
        log = open('log.txt', 'a')
        log.write(link)
        log.write('\n')
        log.close()
