#!/usr/bin/env python
import ffrk_stats
import xlsxwriter

import argparse
ap = argparse.ArgumentParser()
ns = ap.parse_args()


with xlsxwriter.Workbook('stats.xlsx') as wb:
    fmt_bold = wb.add_format({'bold': True})
    for cap in ffrk_stats.Cap:
        charas = ffrk_stats.fetch_all(cap)
        headers = charas[0].keys()

        sheet = wb.add_worksheet(cap.name)
        sheet.write_row(0, 0, headers)
        for i, row in enumerate(charas):
            sheet.write_row(i+1, 0, row.values())

        sheet.freeze_panes(1, 1)
        sheet.add_table(
            0, 0,
            len(charas) + 1, len(headers) - 1,
            {'columns':
                [{'header': h, 'format': fmt_bold} for h in headers],
            },
        )
