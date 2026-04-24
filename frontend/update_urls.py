import os
import re

domain = 'https://madhavi-backend.onrender.com'

def rep(filepath, old, new):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(old, new, content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update app.js
rep('frontend/app.js', r"const API_BASE = '';", f"const API_BASE = '{domain}';")
rep('frontend/app.js', r"fetch\(`\$\{API_BASE\}/enquiry`\)", "fetch(`${API_BASE}/api/enquiry`)")

# Update admin.html
rep('frontend/admin.html', r"const API = '';", f"const API = '{domain}';")

# Update property.html
rep('frontend/property.html', r"fetch\(`/api/properties`\)", f"fetch(`{domain}/api/properties`)")

# Update contact.html
rep('frontend/contact.html', r"fetch\('/enquiry'", f"fetch('{domain}/api/enquiry'")

# Update interiors.html
rep('frontend/interiors.html', r"fetch\('/api/cloudinary/images\?max=200'\)", f"fetch('{domain}/api/cloudinary/images?max=200')")
rep('frontend/interiors.html', r"fetch\('/enquiry'", f"fetch('{domain}/api/enquiry'")

# Update exteriors.html
rep('frontend/exteriors.html', r"fetch\('/api/cloudinary/images\?max=200'\)", f"fetch('{domain}/api/cloudinary/images?max=200')")
rep('frontend/exteriors.html', r"fetch\('/enquiry'", f"fetch('{domain}/api/enquiry'")

print('Replacements done.')
