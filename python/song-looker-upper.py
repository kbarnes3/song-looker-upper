import musicbrainzngs

if __name__ == "__main__":
    print('Hello')

    musicbrainzngs.set_useragent('Song-Looker-Upper', '0.1', 'http://www.kbarnes3.com')

    result = musicbrainzngs.search_recordings('"ALL OF THE LIGHTS" AND artist:"KANYE WEST" AND status:official')
    print(result)