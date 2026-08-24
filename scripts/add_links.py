#!/usr/bin/env python3
import json, urllib.request, urllib.parse, sys

DATA_PATH = 'data/platforms.json'
GITHUB_API = 'https://api.github.com/search/repositories?q='

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    platforms = json.load(f)

for p in platforms:
    if p.get('link'):
        continue
    query = urllib.parse.quote(p['platform'] + ' in:name')
    url = GITHUB_API + query + '&per_page=1'
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.load(resp)
            if data.get('items'):
                p['link'] = data['items'][0].get('html_url')
    except Exception as e:
        # ignore errors, leave link absent
        sys.stderr.write(f'GitHub search failed for {p["platform"]}: {e}\n')

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(platforms, f, indent=2, ensure_ascii=False)
print('Added repository links where found')
