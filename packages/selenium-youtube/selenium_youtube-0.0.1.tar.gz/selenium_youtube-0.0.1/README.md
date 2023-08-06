# selenium_youtube



## Description

selenium implementation of youtube, which can upload/watch/like/comment/pin comment on videos

## Install

~~~~bash
pip install selenium_youtube
# or
pip3 install selenium_youtube
~~~~

## Usage

~~~~python
from selenium_youtube import Youtube

youtube = Youtube(
    'path_to_cookies_folder',
    'path_to_extensions_folder'
)

result = youtube.upload('path_to_video', 'title', 'description', ['tag1', 'tag2'])
~~~~

## Dependencies



## Credits

[Péntek Zsolt](https://github.com/Zselter07)