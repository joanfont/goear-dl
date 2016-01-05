from goear_dl.cli import parser
from goear_dl.utils import get_urls_from_file, validate_file, download_song, download_song_list


def main():

    parse_results = parser.parse_args()
    destination_folder = parse_results.destination

    if parse_results.url:
        song_url = parse_results.url
        download_song(song_url, destination_folder)

    else:  # parse_results.file
        song_file_path = parse_results.file
        parallel = parse_results.parallel
        workers = parse_results.workers
        validate_file(song_file_path)
        song_url_list = get_urls_from_file(song_file_path)
        download_song_list(song_url_list, destination_folder, parallel=parallel, workers=workers)


if __name__ == '__main__':
    main()
