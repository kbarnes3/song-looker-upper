from __future__ import print_function

import musicbrainzngs

DEFAULT_FORMAT = 'Artist: {artist}\nTitle: {title}\nDuration: {duration}\n'


def get_format(format_file_path):
    if format_file_path is None:
        return DEFAULT_FORMAT
    with open(format_file_path, 'r') as format_file:
        format_string = ''
        for line in format_file:
            if len(line) <= 1:
                break
            format_string += line
        return format_string


def lookup_song(format_string, sql):
    musicbrainzngs.set_useragent('Song-Looker-Upper', '0.1', 'http://www.kbarnes3.com')

    result = musicbrainzngs.search_recordings('"BEEN CAUGHT STEALING" AND artist:"JANE\'S ADDICTION" AND status:official')
    recording = result['recording-list'][0]
    artist = recording['artist-credit'][0]['artist']['name']
    artist = artist.replace(u'\u2019', "'")
    title = recording['title']
    title = title.replace(u'\u2019', "'")

    if sql:
        artist = artist.replace("'", "''")
        title = title.replace("'", "''")

    duration = int(int(recording['length']) / 1000)

    output = format_string.format(artist=artist, title=title, duration=duration)
    print(output, end='')
    print('Done')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Looks up song information from')
    parser.add_argument('--format-file', help='Path to a file containing the output format')
    parser.add_argument('--sql', help='Escapes output for SQL commands', action='store_true')
    args = parser.parse_args()

    format_string = get_format(args.format_file)

    lookup_song(format_string, args.sql)
