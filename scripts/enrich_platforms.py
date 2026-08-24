#!/usr/bin/env python3
import json, re, urllib.parse, sys, os

DATA_PATH = 'data/platforms.json'

# Read raw file as text and extract JSON objects safely despite missing commas
raw = open(DATA_PATH, 'r', encoding='utf-8').read()
# Remove surrounding array brackets
inner = raw.strip()[1:-1]
objects = []
buf = ''
brace_depth = 0
for line in inner.splitlines():
    stripped = line.strip()
    if not stripped:
        continue
    # Track braces
    brace_depth += stripped.count('{') - stripped.count('}')
    buf += line + '\n'
    if brace_depth == 0 and buf.strip():
        # Remove trailing comma if present
        obj_str = buf.rstrip(',\n ')
        try:
            obj = json.loads(obj_str)
        except Exception as e:
            sys.stderr.write(f'Failed to parse object: {e}\n{obj_str[:200]}...\n')
            raise
        objects.append(obj)
        buf = ''

# Regex patterns for LaTeX macros
qty_pat = re.compile(r'\\qty\{([^}]+)\}\{\\?([a-zA-Z]+)\}')
qtyprod_pat = re.compile(r'\\qtyproduct\{([^}]+)\}\{\\?mm\}')
weight_pat = re.compile(r'\\weight~\\qty\{([^}]+)\}\{\\?gram\}')
fr_pat = re.compile(r'\\framerate~\\qty\{([^}]+)\}\{\\?Hz\}')
op_pat = re.compile(r'\\operation~\\qty\{([^}]+)\}\{\\?hour\}')

size_pat = re.compile(r'([0-9]+(?:\.[0-9]*)?)\s*(?:×|x)\s*([0-9]+(?:\.[0-9]*)?)\s*(?:×|x)\s*([0-9]+(?:\.[0-9]*)?)\s*mm', re.I)
power_pat = re.compile(r'Power:\s*([0-9]+(?:\.[0-9]*)?)\s*W', re.I)
framerate_pat = re.compile(r'Framerate:\s*([0-9]+(?:\.[0-9]*)?)\s*Hz', re.I)
weight_text_pat = re.compile(r'Weight:\s*([0-9]+(?:\.[0-9]*)?)\s*g', re.I)
operation_pat = re.compile(r'Operation:\s*([0-9]+(?:\.[0-9]*)?)\s*h', re.I)

for p in objects:
    specs = p.get('specifications', '')
    # Replace LaTeX macros
    specs = qty_pat.sub(lambda m: f"{m.group(1)} {m.group(2)}", specs)
    specs = qtyprod_pat.sub(lambda m: f"{m.group(1).replace(' ', '×')} mm", specs)
    specs = weight_pat.sub(lambda m: f"Weight: {m.group(1)} g", specs)
    specs = fr_pat.sub(lambda m: f"Framerate: {m.group(1)} Hz", specs)
    specs = op_pat.sub(lambda m: f"Operation: {m.group(1)} h", specs)
    specs = re.sub(r'\\[a-zA-Z]+~', '', specs)
    specs = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', specs)
    specs = re.sub(r'\s+', ' ', specs).strip()
    p['specifications'] = specs
    # Extract fields into separate keys
    fr = framerate_pat.search(specs)
    if fr:
        p['framerate'] = f"{fr.group(1)} Hz"
    wt = weight_text_pat.search(specs)
    if wt:
        p['weight'] = f"{wt.group(1)} g"
    op = operation_pat.search(specs)
    if op:
        p['operation'] = f"{op.group(1)} h"
    sz = size_pat.search(specs)
    if sz:
        p['size'] = f"{sz.group(1)}×{sz.group(2)}×{sz.group(3)} mm"
    pw = power_pat.search(specs)
    if pw:
        p['power'] = f"{pw.group(1)} W"
    # Ensure image_url
    if not p.get('image_url'):
        p['image_url'] = f"https://source.unsplash.com/400x300/?ultrasound,{urllib.parse.quote(p['platform'])}"

# Write back pretty JSON array
with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(objects, f, indent=2, ensure_ascii=False)
print('Enriched platforms.json')
