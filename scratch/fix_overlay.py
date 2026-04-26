import glob
import re

html_files = glob.glob('c:/Users/srini/Downloads/madhavi enterprises/frontend/*.html')

def update_file(filepath):
    filename = filepath.split('\\')[-1]
    if filename in ["index.html", "admin.html"]:
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the hero class
    match = re.search(r'\.(int-hero|prop-hero|ventures-hero|contact-hero)\s*\{', content)
    if match:
        hero_class = match.group(1)
        
        # Replace the existing ::before block with a dark overlay
        # Example: .int-hero::before { ... }
        content = re.sub(
            r'\.' + hero_class + r'::before\s*\{[^}]+\}',
            f'.{hero_class}::before {{ content:""; position:absolute; inset:0; background:rgba(0,0,0,0.6); z-index:0; }}',
            content
        )
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed overlay in {filename}")

for f in html_files:
    update_file(f)
