import os
import re
import typing

import bs4
import requests
import youtube_dl
import prettytable

from . import utils
from . import loggers

BASE_YOUTUBE_URL = 'http://www.youtube.com'
BASE_YOUTUBE_SEARCH_URL = BASE_YOUTUBE_URL + '/results?search_query={}'

table = prettytable.PrettyTable()
table.field_names = ['id', 'title', 'video link']


def wtm(song_name: str = None, select_top_result: bool = False) -> typing.Tuple[str, bool]:
    search_query: str = '+'.join([word for word in re.split(r'\s', song_name) if len(word)])
    response: requests.Response = requests.get(BASE_YOUTUBE_SEARCH_URL.format(search_query))

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        titles: typing.List[typing.Tuple[str, str, str]] = []
        # Kind of a complex data structure -
        #     [(Title #1, link for #1, thumbnail url for #1),
        #      (Title #2, link for #2, thumbnail url for #1),
        #      (Title #3, link for #3, thumbnail url for #1),]

        for index, title in enumerate(soup.findAll(attrs={'class': 'yt-uix-tile-link'})):
            link = BASE_YOUTUBE_URL + title['href']
            table.add_row([index + 1, title.text, link])
            thumbnail_url = 'http://img.youtube.com/vi/{}/0.jpg'.format(
                re.findall(r'^.*((youtu.be/)|(v/)|(/u/\w/)|(embed/)|(watch\?))\??v?=?([^#&?]*).*', link)[-1][-1]
            )
            titles.append((title.text, link, thumbnail_url))

        print(table)

        if select_top_result:
            option = 1
        else:
            try:
                option = input('\nEnter most relevant title id : ')
            except KeyboardInterrupt:
                return '\nInterrupted.', False

        try:
            option = int(option)
        except ValueError:
            return 'Please enter a valid id.', False

        if option <= 0 or option > len(titles):
            return 'Please enter a valid id.', False

        postprocessors: typing.List[typing.Dict[str, str]] = [
            {
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                'key': 'FFmpegExtractAudio',
            }
        ]

        dir_listing_before_downloading = os.listdir('.')

        with youtube_dl.YoutubeDL(
            {
                'postprocessors': postprocessors,
                'logger': loggers.LowVerbosityLogger(),
                'progress_hooks': [utils.progress_hook],
            }
        ) as ydl:
            utils.get_thumbnail(titles[option - 1][2])
            ydl.download([titles[option - 1][1]])

        new_file_name = utils.get_new_file_name(set(dir_listing_before_downloading))
        utils.assign_thumbnail('thumbnail.jpg', new_file_name)
        os.rename(new_file_name, titles[option - 1][0] + '.mp3')
        os.remove('thumbnail.jpg')

        return 'done.', True

    else:
        return 'Error from YouTube\'s side.', False
