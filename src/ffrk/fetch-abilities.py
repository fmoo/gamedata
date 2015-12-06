import argparse
from collections import OrderedDict
from ffrk_utils import requests_get_html

ap = argparse.ArgumentParser()
ap.add_argument('mode', choices=['csv', 'json'])
ns = ap.parse_args()


doc = requests_get_html('http://ffrk.kongbakpao.com/character-usable-abilities/')
tables = doc.xpath('//table')
assert len(tables) > 0, 'Unable to find table in body'
assert len(tables) == 1, 'Too many tables in body'
table = tables[0]

labels = map(
    lambda d: d.text,
    table.xpath('thead//th'),
)

rows = table.xpath('tbody//tr')
charas = OrderedDict()
for row in rows:
    chara = {}
    cols = row.xpath('td')
    for i, col in enumerate(cols):
        k = labels[i]
        try:
            chara[k] = int(col.text)
        except:
            chara[k] = col.text
        if col.text is None:
            chara[k] = 0

    charas[chara['Character']] = chara

if ns.mode == 'json':
    import json
    print json.dumps(charas, indent=2)

elif ns.mode == 'csv':
    import StringIO
    import csv

    buf = StringIO.StringIO()
    dw = csv.DictWriter(buf, labels)
    dw.writeheader()
    dw.writerows(charas.values())
    print buf.getvalue()
