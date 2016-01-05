import argparse
from goear_dl import __version__
import multiprocessing

pool_size = 2 * multiprocessing.cpu_count()

parser = argparse.ArgumentParser('goear-dl')

version = '%(prog)s {version}'.format(version=__version__)

source_group = parser.add_mutually_exclusive_group(required=True)
source_group.add_argument('-u', action='store', dest='url', help='URL of the song to download')
source_group.add_argument('-f', action='store', dest='file', help='Path of the URLs file')

parallel_group = parser.add_argument_group()
parallel_group.add_argument('-p', action='store_true', dest='parallel', default=False,
                            help='Download song list in parallel mode')
parallel_group.add_argument('-w', action='store', dest='workers', default=pool_size,
                            help='Number of processes')

parser.add_argument('-d', action='store', dest='destination', default='', help='File\'s destination folder')
parser.add_argument('--version', action='version', version=version)
