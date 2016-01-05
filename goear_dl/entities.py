class BaseEntity:
    pass


class Song(BaseEntity):
    def __init__(self, song_id=None, title=None, artist=None, bit_rate=None, length=0, url=None):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.bit_rate = bit_rate
        self.length = length
        self.url = url

        self.file_name = '{title} - {artist}.mp3'.format(title=self.title, artist=self.artist)

    @staticmethod
    def get_length_from_string(length_string):
        length_parts = length_string.split(':')
        return int(length_parts[0]) * 60 + int(length_parts[1]) if len(length_parts) == 2 else None

    def __str__(self):
        return '{title} - {artist}'.format(title=self.title, artist=self.artist)
