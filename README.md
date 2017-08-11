# Treehouse video downloader

## Summary
Treehouse Video Downloader downloads videos (with optional subtitles) from the specified [Treehouse courses and workshops](http://www.teamtreehouse.com).

## Dependencies
Install these dependencies:
- [youtube-dl](https://rg3.github.io/youtube-dl/)
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Usage
Before usage you need to
- change the **USERNAME** and **PASSWORD** variables in `main.py` file and
- define the **courses/workshops** you would like to download in the `links.txt` file. Example list of the courses/workshops is available.

If you would like to download the **subtitles** of the videos set `SUBTITLES = True`. They are not downloaded by default.

If the **download of the video fails**, the course URL will be saved in `log.txt`.

## Notes
Because youtube-dl login does not work for proper authentication of the Treehouse user I have used python 'requests' module to get the correct video link.

Hopefully youtube-dl will be extended to cover Treehouse soon. Here is the [issue](https://github.com/rg3/youtube-dl/issues/9836).

Script was tested with the `youtube-dl 2017.07.30.1` and `python 3.5.3`.
