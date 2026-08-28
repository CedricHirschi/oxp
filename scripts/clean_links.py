#!/usr/bin/env python3
import json, re, sys

def clean_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for p in data:
        dl = p.get('data_link','')
        # Remove backslashes, curly braces, and stray commas
        dl = dl.replace('\\,', ',')
        dl = dl.replace('\\', '')
        dl = dl.replace('{','').replace('}','')
        dl = dl.replace(',,', ',')
        # Remove trailing commas and spaces
        dl = re.sub(r',\s*,+', ',', dl)
        dl = dl.strip(', ')
        p['data_link'] = dl
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Cleaned {path}')

clean_file('data/platforms.json')
