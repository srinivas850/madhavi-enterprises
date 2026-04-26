import glob
import re

html_files = glob.glob('c:/Users/srini/Downloads/madhavi enterprises/frontend/*.html')

# Hero images for different pages to make them realistic
images = {
    'interiors.html': 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1920&q=80',
    'exteriors.html': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1920&q=80',
    'properties.html': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1920&q=80',
    'ventures.html': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=1920&q=80',
    'contact.html': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&q=80',
    'admin.html': '', # Admin doesn't need hero
    'property.html': ''
}

def update_file(filepath):
    filename = filepath.split('\\')[-1]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove body background dark color
    content = re.sub(r'body\s*\{\s*background:\s*#[0-9a-fA-F]+;\s*\}', '', content)
    content = re.sub(r'body\s*\{\s*background-color:\s*#[0-9a-fA-F]+;\s*\}', '', content)

    # 2. Update hero backgrounds with images
    if filename in images and images[filename]:
        bg_url = images[filename]
        # Replace hero css in <style> block
        # For interiors.html: .int-hero { ... background: ... }
        # Match .int-hero, .prop-hero, .hero-section
        content = re.sub(
            r'(\.(?:int-hero|prop-hero|ventures-hero|contact-hero|hero-custom)\s*\{[^}]*?)background:\s*[^;]+;',
            r"\1background: url('" + bg_url + r"') center/cover no-repeat; position: relative;",
            content,
            flags=re.DOTALL
        )
        # Ensure there is a dark overlay so text is readable
        overlay_css = r"\n    .\2::before {\n      content:'';\n      position:absolute;\n      inset:0;\n      background: rgba(0,0,0,0.6);\n      z-index: 0;\n    }\n    .\2-content { position:relative; z-index:1; }\n"
        
        # We need to find the hero class name and add ::before
        match = re.search(r'\.(int-hero|prop-hero|ventures-hero|contact-hero|hero-custom)\s*\{', content)
        if match:
            hero_class = match.group(1)
            # Add overlay if not exists
            if f'.{hero_class}::before' not in content:
                 content = re.sub(r'(\.' + hero_class + r'\s*\{[^}]+\})', r'\1\n    .' + hero_class + r'::before { content:""; position:absolute; inset:0; background:rgba(0,0,0,0.6); z-index:0; }', content)
                 
    # 3. Fix hardcoded dark gradients in inline styles
    content = re.sub(r'style="background:\s*linear-gradient[^"]+"', 'style="background: #FFFFFF;"', content)
    content = re.sub(r'background:\s*linear-gradient\([^)]+#050B18[^)]+\);?', 'background: #FFFFFF;', content)
    
    # 4. Remove dark background from forms or contact wrapper
    content = re.sub(r'\.contact-wrapper\s*\{\s*background:\s*#[0-9a-fA-F]+;', '.contact-wrapper { background: #FFFFFF;', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")

for f in html_files:
    if "index.html" not in f:
        update_file(f)
