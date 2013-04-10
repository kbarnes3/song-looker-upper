from __future__ import print_function
import csv
import sys

import musicbrainzngs

DEFAULT_FORMAT = 'Artist: {artist}\nTitle: {title}\nDuration: {duration}\n'


class RecordParseException(Exception):
    pass


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


def lookup_songs(csv_path, format_string, sql):
    with open(csv_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            try:
                lookup_song(row[0], row[1], format_string, sql)
            except RecordParseException:
                pass


def lookup_song(artist, title, format_string, sql):
    musicbrainzngs.set_useragent('Song-Looker-Upper', '0.1', 'http://www.kbarnes3.com')

    query = '"{0}" AND artist:"{1}" AND status:official'.format(title, artist)

    result = musicbrainzngs.search_recordings(query)

    if len(result['recording-list']) < 1:
        print('No songs found for query ' + query, file=sys.stderr)
        return

    recording = result['recording-list'][0]

    try:
        artist = recording['artist-credit'][0]['artist']['name']
        artist = artist.replace(u'\u2019', "'")
        title = recording['title']
        title = title.replace(u'\u2019', "'")

        if sql:
            artist = artist.replace("'", "''")
            title = title.replace("'", "''")

        length = recording['release-list'][0]['medium-list'][1]['track-list'][0]['length']
        duration = int(int(length) / 1000)

        output = format_string.format(artist=artist, title=title, duration=duration)
        print(output, end='')
    except Exception as ex:
        print('Error handling recording: ' + str(recording), file=sys.stderr)
        print(ex.message, file=sys.stderr)
        raise RecordParseException(ex.message)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Looks up song information from')
    parser.add_argument('CSV_FILE', help='A CSV file of artist, song pairs on each line')
    parser.add_argument('--format-file', help='Path to a file containing the output format')
    parser.add_argument('--sql', help='Escapes output for SQL commands', action='store_true')
    args = parser.parse_args()

    format_string = get_format(args.format_file)

    lookup_songs(args.CSV_FILE, format_string, args.sql)
