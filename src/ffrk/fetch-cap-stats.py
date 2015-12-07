import ffrk_stats
from ffrk_utils import enum_names

import argparse
ap = argparse.ArgumentParser()
ap.add_argument('cap', choices=enum_names(ffrk_stats.Cap))
ap.add_argument('mode', choices=['csv', 'json'])
ns = ap.parse_args()

charas = ffrk_stats.fetch_all(ffrk_stats.Cap[ns.cap])

if ns.mode == 'json':
    import json
    print json.dumps(charas, indent=2)

elif ns.mode == 'csv':
    import StringIO
    import csv

    buf = StringIO.StringIO()
    dw = csv.DictWriter(buf, charas[0].keys())
    dw.writeheader()
    dw.writerows(charas)
    print buf.getvalue()
