# Treehouse video downloader

## Summary
Treehouse Video Downloader downloads videos from the specified [Treehouse links](http://www.treehouseteam.com).

## Dependencies
- youtube-dl
- BeautifulSoup 4

## Usage
To use it change the **USERNAME** and **PASSWORD** variables in `main.py` file and define
the **links** you would like to download in the `links.txt` file. Example list of the files is available.

If the **download of the video fails**, the link will be saved in `log.txt`.

##Notes
Because youtube-dl login does not work for proper authentication of the Treehouse user I have used python 'requests' module to get the correct video link.

Hopefully youtube-dl will be extended to cover Treehouse soon. Here is the [issue](https://github.com/rg3/youtube-dl/issues/9836).

Script tested on the youtube-dl version 2016.07.28 and python 3.4.
