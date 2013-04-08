import musicbrainzngs


def lookup_song(sql):
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

    format_string = "INSERT INTO SONGS (artist, title, duration) VALUES ('{0}', '{1}', {2})"
    output = format_string.format(artist, title, duration)
    print(output)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Looks up song information from')
    parser.add_argument('--sql', help='Escapes output for SQL commands', action='store_true')
    args = parser.parse_args()

    lookup_song(args.sql)
