from enum import Enum
from ffrk_utils import requests_get_html
from collections import OrderedDict
import lxml.etree


class Stat(Enum):
    ATTACK = 'Attack'
    DEFENSE = 'Defense'
    MAGIC = 'Magic'
    MIND = 'Mind'
    HP = 'HP'
    RESISTANCE = 'Resistance'
    SPEED = 'Speed'

class Cap(Enum):
    LV50 = ''
    LV65 = 'Lv%2065%20'
    LV80 = 'Lv%2080%20'

def stat_url(stat, cap=Cap.LV50):
    return (
        'https://ffrkstrategy.gamematome.jp/game/951/wiki/'
        'Character_Rankings_%s%s%%20Ranking' %
        (cap.value, stat.value)
    )

def fetch(stat, cap=Cap.LV50):
    url = stat_url(stat, cap)
    doc = requests_get_html(url)

    tables = doc.xpath('//table')
    assert len(tables) > 0, 'Unable to find table in body'
    assert len(tables) == 1, 'Too many tables in body'
    table = tables[0]

    headers = map(
        lambda d: d.text,
        table.xpath('tbody//th'),
    )

    charas = OrderedDict()
    for row in table.xpath('tbody//tr[td]'):
        chara = {}
        cols = row.xpath('td')
        for i, col in enumerate(cols):
            k = headers[i]
            if k in ['Image', 'Ranking']:
                continue
            if k == 'Character':
                col = col.xpath('a')[0]

            value = lxml.etree.tostring(col, method='text')
            try:
                chara[k] = int(value)
            except:
                chara[k] = value
        charas[chara['Character']] = chara[stat.value]
    return charas

def fetch_all(cap=Cap.LV50):
    allstats = OrderedDict()
    for stat in Stat:
        d = fetch(stat=stat, cap=cap)
        for k, v in d.items():
            if k not in allstats:
                allstats[k] = OrderedDict(Character=k)

            allstats[k][stat.value] = v
    return allstats.values()
