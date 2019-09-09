"""
Treehouse Video Downloader downloads videos from
the specified Treehouseteam.com courses and workshops.

To use it change the username and password in this file
and define the course/workshop you would like to download
in the links.txt file.

You can change the format - default is mp4, but you can
also get webm, just change VIDEO_FORMAT = 'webm' below.

If you would like to download the subtitles of the
videos set `SUBTITLES = True`. They are not downloaded
by default.

If download fails, the link will be saved in log.txt
"""

import os
import re
import requests

from bs4 import BeautifulSoup
import youtube_dl

USERNAME = 'your_username'
PASSWORD = 'your_password'

# Download subtitles of the videos - use 'True' to download subtitles
SUBTITLES = True

# Download teachner's notes of the videos to html file - use 'True' to download
TEACHER_NOTES = True

# Download accelerator
EXTERNAL_DL = 'aria2c'

# Video format - webm or mp4
VIDEO_FORMAT = 'mp4'

HOME_DIR = os.getcwd()


def do_auth(user, pwd):
    """Login using username and password, returns logged in session
    Source: https://github.com/dx0x58/Treehouse-dl
    """
    sess = requests.Session()

    login_page = sess.get('https://teamtreehouse.com/signin')
    login_page_soup = BeautifulSoup(login_page.text, "html.parser")

    token_val = login_page_soup.find(
        'input', {'name': 'authenticity_token'}).get('value')
    utf_val = login_page_soup.find('input', {'name': 'utf8'}).get('value')

    post_data = {'user_session[email]': user, 'user_session[password]': pwd, 'utf8': utf_val,
                 'authenticity_token': token_val}

    profile_page = sess.post(
        'https://teamtreehouse.com/person_session', data=post_data)

    profile_page_soup = BeautifulSoup(profile_page.text, "html.parser")
    auth_sign = profile_page_soup.title.text
    if auth_sign:
        if auth_sign.lower().find('home') != -1:
            print('[!] Login success!')
        else:
            print('[!!] Not found login attribute\nExit...')
            sys.exit(0)
    else:
        raise Exception('Login failed!')

    return sess


def http_get(url):
    """Returns text of url
    Source: https://github.com/dx0x58/Treehouse-dl
    """
    resp = sess.get(url)
    return resp.text


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
    html = http_get(link)
    soup = BeautifulSoup(html, "html.parser")

    for id in soup.select("div#questions-container > ul"):
        return id.attrs["data-step-id"]


def removeReservedChars(value):
    """ Remove reserved characters because of Windows OS compatibility
    """
    return "".join(i for i in value if i not in r'\/:*?"<>|')


def getSubtitles(id, name):
    """ Download and rename subtitle file to match the downloaded videos.
    Subtitle is located at https://teamtreehouse.com/videos/{id}}/captions
    """
    subtitlesLink = 'https://teamtreehouse.com/videos/{}/captions'.format(id)
    response = requests.get(subtitlesLink)
    if response.status_code == 200:
        contentDisposition = response.headers['Content-Disposition']
        parts = contentDisposition.split('"')
        filename = removeReservedChars(parts[-2])
        title = '{}-{}'.format(name, filename)
        content = response.text
        with open(title, 'w') as f:
            f.write(content)
        return 0

def getTeacherNotes(soup, name):
    try: 
        fullHtml = "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"> \
        <div class=\"grid-70 tablet-grid-65 videos-show\">" + \
        soup.select("#video-meta")[0].prettify() + "</div>" + \
        soup.select(".teachers-notes-container .grid-70")[0].prettify()
        title = '{}{}'.format(name, ".html")
        with open(title, 'w') as f:
            f.write(fullHtml)
        return 0
    except Exception as e:
        print(e)

def getVideoFormat():
    """ Validate video format or return default format
    """
    default = 'mp4'
    if (VIDEO_FORMAT == 'mp4' or VIDEO_FORMAT == 'webm'):
        return VIDEO_FORMAT
    else:
        return default


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
    sess = do_auth(USERNAME, PASSWORD)

    try:
        link = link.strip()
        print('Downloading: {}'.format(link))

        videos = getLinksWorkshop(link) or getLinkWorkshop(
            link) or getLinksCourse(link)

        # Generate folder name and move to it
        parts = link.split('/')
        title = parts[-1]
        move_to_course_directory(title)

        for video in videos:
            html = http_get(video)
            soup = BeautifulSoup(html, "html.parser")

            # Extract title for filename
            h1 = soup.h1.contents[0]

            # Output with the title of the video
            output = u'%(id)s-' + removeReservedChars(h1) + u'.%(ext)s'

            # Video source link
            tag = soup.video
            videolink = tag.find_all(
                type="video/{}".format(getVideoFormat()))[0].get('src')

            # Youtube-dl options
            options = {
                'outtmpl': output, 'external_downloader': EXTERNAL_DL
                # ,'verbose': True
            }

            with youtube_dl.YoutubeDL(options) as ydl:

                ydl.download([videolink])

                if (SUBTITLES):
                    ID = getID(video)
                    info = ydl.extract_info(videolink, download=False)
                    name = info.get('title', None)
                    subs = getSubtitles(ID, name)

                if (TEACHER_NOTES):
                    info = ydl.extract_info(videolink, download=False)
                    name = info.get('title', None)
                    notes = getTeacherNotes(soup, name + removeReservedChars(h1))

    except:
        os.chdir(HOME_DIR)
        log = open('log.txt', 'a')
        log.write(link)
        log.write('\n')
        log.close()
