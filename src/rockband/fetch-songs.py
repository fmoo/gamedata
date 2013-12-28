#!/usr/bin/env python


def main():
    import requests
    resp = requests.get('http://www.rockband.com/services.php/music/all-songs.json')

    with open('all-songs.json', mode='w') as f:
        f.write(resp.content)

if __name__ == '__main__':
    main()
