#!/usr/bin/env python3
import json, re, urllib.parse, sys
DATA_PATH = 'data/platforms.json'
# Load JSON safely (handle missing commas already fixed)
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    platforms = json.load(f)
# Patterns
qty_pat = re.compile(r'\\qty\{([^}]+)\}\{\\?([a-zA-Z]+)\}')
qtyprod_pat = re.compile(r'\\qtyproduct\{([^}]+)\}\{\\?mm\}')
weight_pat = re.compile(r'\\weight~\\qty\{([^}]+)\}\{\\?gram\}')
fr_pat = re.compile(r'\\framerate~\\qty\{([^}]+)\}\{\\?Hz\}')
op_pat = re.compile(r'\\operation~\\qty\{([^}]+)\}\{\\?hour\}')

def clean_text(s: str) -> str:
    """Remove LaTeX markup from a string.

    Handles the specific patterns used in the catalog, such as
    \qty{value}{unit}, \qtyproduct{value}{mm}, weight, framerate, and operation
    macros, as well as generic LaTeX commands, math delimiters, citations,
    and non‑breaking spaces.
    """
    # Quantity patterns
    s = qty_pat.sub(lambda m: f"{m.group(1)} {m.group(2)}", s)
    s = qtyprod_pat.sub(lambda m: f"{m.group(1).replace(' ', '×')} mm", s)
    s = weight_pat.sub(lambda m: f"Weight: {m.group(1)} g", s)
    s = fr_pat.sub(lambda m: f"Framerate: {m.group(1)} Hz", s)
    s = op_pat.sub(lambda m: f"Operation: {m.group(1)} h", s)

    # Approximate symbol within math mode
    s = re.sub(r'\$\\approx\$', '≈', s)
    # Remove any remaining $...$ math, keeping inner text without backslashes
    s = re.sub(r'\$(.*?)\$', lambda m: m.group(1).replace('\\', ''), s)
    # Remove citations
    s = re.sub(r'\\cite\{[^}]*\}', '', s)
    # Remove generic LaTeX commands (with optional argument)
    s = re.sub(r'\\[a-zA-Z]+(?:\{[^}]*\})?', '', s)
    # Remove stray LaTeX spacing commands (~, \,, \; etc.) and tildes used for non‑breaking space
    s = s.replace('~', ' ')
    # Collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

for p in platforms:
    # Clean each string field in the entry
    for key, value in list(p.items()):
        if isinstance(value, str):
            p[key] = clean_text(value)
    # Ensure image_url if missing (after cleaning platform name)
    if not p.get('image_url'):
        p['image_url'] = f"https://source.unsplash.com/400x300/?ultrasound,{urllib.parse.quote(p['platform'])}"

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(platforms, f, indent=2, ensure_ascii=False)
print('Cleaned LaTeX tags and ensured image_url')
