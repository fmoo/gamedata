import urllib
import os.path
import requests
import html5lib

def enum_names(cls):
    return [e.name for e in cls]

def enum_values(cls):
    return [e.value for e in cls]

def requests_get(url):
    cachefile = os.path.join('cache', urllib.quote(url, ''))
    if os.path.exists(cachefile):
        with open(cachefile, mode='rb') as f:
            return f.read()

    resp = requests.get(url)
    resp.raise_for_status()
    with open(cachefile, mode='w') as f:
        f.write(resp.content)

    return resp.content

def requests_get_html(url):
    return html5lib.parse(
        requests_get(url),
        treebuilder='lxml',
        namespaceHTMLElements=False,
    )
