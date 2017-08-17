# Treehouse video downloader

## Summary
Treehouse Video Downloader downloads videos (with optional subtitles) from the specified [Treehouse courses and workshops](http://www.teamtreehouse.com).

## Dependencies
Install these dependencies:
- [requests](http://docs.python-requests.org/en/master/)
```
pip install requests
```
- [youtube-dl](https://rg3.github.io/youtube-dl/)
```
pip install youtube_dl
```
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
```
pip install beautifulsoup4
```

## Usage

1. Add your credentials to `main.py` file
```
USERNAME = 'your_username'
PASSWORD = 'your_password'
```
2. define the **courses/workshops** you would like to download in the `links.txt` file. Example list of the courses/workshops is already in the file.
3. Go to file directory where `main.py` and `links.txt` are saved and run `main.py` from the terminal with:
```python main.py```
4. Wait until all videos are downloaded and have fun watching them.

If the **download of the video fails**, the course URL will be saved in `log.txt`.

## Subtitles

If you would like to:
- download the **subtitles** of the videos set `SUBTITLES = True`. They are not downloaded by default.
- download ONLY subititles and not the videos set `SUBTITLES = True` and comment out the line that downloads the video
```
# ydl.download([videolink])
```

## Downloader

Default downloader is `aria2c`. If you wish to change it, edit `EXTERNAL_DL = 'aria2c'`

## Additional options

You can extend the script by adding options in the `options` variable:
```
options = {
    'outtmpl': output,
    'external_downloader': EXTERNAL_DL
    # ,'verbose': True
}
```

Here is the list of all options (however not all of them work): https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L129-L290

Feel free to experiment and test.

## Notes
Because youtube-dl login does not work for proper authentication of the Treehouse user I have used python 'requests' module to get the correct video link.

Hopefully youtube-dl will be extended to cover Treehouse soon. Here is the [issue](https://github.com/rg3/youtube-dl/issues/9836).

You can upgrade `youtube-dl` with `sudo youtube-dl -U`

Script was tested with the `youtube-dl 2017.08.13` and `python 3.5.3`.
