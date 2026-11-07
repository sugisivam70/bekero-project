import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
missing = []
total_refs = 0
found_refs = set()

for hf in sorted(html_files):
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'''(?:src=["']|url\(["']?)(images/[^"'\)]+)''', content)
    for m in matches:
        total_refs += 1
        clean_path = m.split('?')[0].split('#')[0]
        full_path = os.path.normpath(os.path.join('.', clean_path))
        found_refs.add(clean_path)
        if not os.path.isfile(full_path):
            missing.append((hf, clean_path))

# Check css/style.css
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()
css_matches = re.findall(r'''url\(["']?([^"'\)]+)["']?\)''', css)
for m in css_matches:
    if 'fonts.googleapis' in m or 'data:' in m:
        continue
    full_path = os.path.normpath(os.path.join('css', m))
    if not os.path.isfile(full_path):
        missing.append(('css/style.css', m))

print(f"Total image references checked: {total_refs}")
print(f"Unique image files referenced: {len(found_refs)}")
if missing:
    print(f"MISSING ASSETS ({len(missing)}):")
    for hf, p in missing:
        print(f"  {hf} -> {p}")
else:
    print("SUCCESS: ALL ASSETS (HTML + CSS) EXIST ON DISK! ZERO 404s.")
