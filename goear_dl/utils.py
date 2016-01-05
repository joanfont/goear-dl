import functools
import re
import os

import sys

from goear_dl.core import SongNotFoundError, GoearEngine, GoearSearch

import multiprocessing


def get_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        urls = f.readlines()
    return urls


# Django URL regex
# http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
url_regex = re.compile(
        r'^(?:http)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def print_error(error, with_exit=False):
    print(error, file=sys.stderr)
    if with_exit:
        sys.exit(1)


def validate_file(file_path):
    if not os.path.exists(file_path):
        file_does_not_exists_error = 'File {file_path} does not exists in the filesystem'.format(file_path=file_path)
        print_error(file_does_not_exists_error, with_exit=True)

    if os.path.isdir(file_path):
        path_is_dir = 'File path must be a file, not a directory'
        print_error(path_is_dir)


def download_song(song_url, destination_folder):

    if not url_regex.match(song_url):
        url_malformed = 'The URL {song_url} seems to be malformed'.format(song_url=song_url)
        print_error(url_malformed, with_exit=True)

    song = GoearSearch.find_by_url(song_url)

    try:
        downloading_str = 'Downloading {song}...'.format(song=song)
        print(downloading_str, file=sys.stdout)

        GoearEngine.download(song, destination_folder=destination_folder)

        complete_str = 'Download of {song} complete!'.format(song=song)
        print(complete_str, file=sys.stdout)
    except SongNotFoundError as ex:
        song_not_found_str = 'Song {song_url} not found, maybe the URL is wrong'.format(song_url=song)
        print_error(song_not_found_str, with_exit=True)


def download_song_list(song_url_list, destination_folder, parallel=False, workers=1):

    download_song_fnx = functools.partial(download_song, destination_folder=destination_folder)

    if parallel:
        pool = multiprocessing.Pool(workers)
        pool.map(download_song_fnx, song_url_list)
    else:
        for song_url in song_url_list:
            download_song_fnx(song_url)

