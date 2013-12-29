#!/usr/bin/env python


def main():
    import requests
    resp = requests.get('http://www.dancecentral.com/wp-content/themes/turbo/songs-helper.php')

    with open('all-songs.json', mode='w') as f:
        f.write(resp.content)

if __name__ == '__main__':
    main()
