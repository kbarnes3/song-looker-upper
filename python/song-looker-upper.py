import musicbrainzngs

if __name__ == "__main__":
    musicbrainzngs.set_useragent('Song-Looker-Upper', '0.1', 'http://www.kbarnes3.com')

    result = musicbrainzngs.search_recordings('"ALL OF THE LIGHTS" AND artist:"KANYE WEST" AND status:official')
    recording = result['recording-list'][0]
    artist = recording['artist-credit'][0]['artist']['name']
    artist = artist.replace("'", "''")
    title = recording['title']
    title = title.replace("'", "''")
    duration = int(int(recording['length']) / 1000)

    format_string = "INSERT INTO SONGS (artist, title, duration) VALUES ('{0}', '{1}', {2})"
    output = format_string.format(artist, title, duration)
    print(output)
