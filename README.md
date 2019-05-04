# Treehouse video downloader

## Summary
Treehouse Video Downloader downloads videos (with optional subtitles) from the specified [Treehouse courses and workshops](http://www.teamtreehouse.com).


## Dependencies
Install all dependencies:
```
pip install -r requirements.txt
```
or install them separately
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
3. Go to file directory where `main.py` and `links.txt` are saved and run `main.py` from the terminal with: `python main.py`
4. Wait until all videos are downloaded and have fun watching them.

If the **download of the video fails**, the course URL will be saved in `log.txt`.

## Options
### Subtitles

If you would like to:
- download the **subtitles** of the videos set `SUBTITLES = True`. They are not downloaded by default.
- download ONLY subititles and not the videos set `SUBTITLES = True` and comment out the line that downloads the video
```
# ydl.download([videolink])
```

### Video format
The default video format is webm, but you can
also get mp4 files, just change `VIDEO_FORMAT = 'mp4'` in the `main.py` script.

One of the users noticed mp4 video format downloads only 30 sec clips so test it to make sure mp4 format is available for a particular course. 

### Downloader

Default downloader is `aria2c`. If you wish to change it, edit `EXTERNAL_DL = 'aria2c'`

### Additional options

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

You can upgrade `youtube-dl` with `sudo -H pip install --upgrade youtube-dl`

Upgraded on 4 May with 2 functions from project https://github.com/dx0x58/Treehouse-dl

Script was tested with the `youtube-dl 2019.4.30` and `Python 3.6.7`.

