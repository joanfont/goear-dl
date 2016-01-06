goear-dl
========

download songs from goear

## Installation

Install using pip:

	sudo pip install goear-dl

## Usage

To download a song given its URL:

	goear-dl -u http://www.goear.com/listen/9fae988/mr-blue-sky-electric-light-orchestra
	
You can specify an output folder using the `-d` parameter:
	
	goear-dl -u http://www.goear.com/listen/9fae988/mr-blue-sky-electric-light-orchestra -d /home/user/Music/

	
You can download a list of songs using the parameter `-f`:

	goear-dl -f path/to/song_list.txt
	
	
This file has to contain an URL per line:


	http://www.goear.com/listen/9fae988/mr-blue-sky-electric-light-orchestra
	http://www.goear.com/listen/2f1b121/confusion-electric-light-orchestra-elo
	http://www.goear.com/listen/7deba5d/shangri-la-electric-light-orchestra
	
If you chose to download an URL list you can do it in parallel mode. Use `-p` switch to enable-it:

	goear-dl -f path/to/song_list.txt -p
	
If you want to specify the number of workers use the `-w` option. By default will use `2 * cpu_count`:

	goear-dl -f path/to/song_list.txt -p -w 3

## Authors

[Joan Font](https://www.joan-font.cat) ([@joanfont](https://github.com/joanfont)) created goear-dl
