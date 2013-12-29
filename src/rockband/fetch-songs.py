#!/usr/bin/env python


def main():
    import requests
    # This json endpoint is fetched by http://www.rockband.com/songs/finder
    resp = requests.get('http://www.rockband.com/services.php/music/all-songs.json')

    with open('all-songs.json', mode='w') as f:
        f.write(resp.content)

if __name__ == '__main__':
    main()
