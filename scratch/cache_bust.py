import glob
import re

html_files = glob.glob('c:/Users/srini/Downloads/madhavi enterprises/frontend/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'href="style.css?v=4"' in content:
        content = content.replace('href="style.css?v=4"', 'href="style.css?v=5"')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Busted cache to v5 in {filepath}")
