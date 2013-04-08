import musicbrainzngs

DEFAULT_FORMAT = 'Artist: {0}\nTitle: {1}\nDuration: {2}'


def get_format(format_file_path):
    if format_file_path is None:
        return DEFAULT_FORMAT
    return DEFAULT_FORMAT

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

    output = format_string.format(artist, title, duration)
    print(output)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Looks up song information from')
    parser.add_argument('--format-file', help='Path to a file containing the output format')
    parser.add_argument('--sql', help='Escapes output for SQL commands', action='store_true')
    args = parser.parse_args()

    format_string = get_format(args.format_file)

    lookup_song(format_string, args.sql)
