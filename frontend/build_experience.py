import glob
import re

# 1. Create experience.html from interiors.html
with open('interiors.html', 'r', encoding='utf-8') as f:
    exp_content = f.read()

# Replace titles and hero section
exp_content = re.sub(r'<title>.*?</title>', '<title>Experience - Madhavi Enterprises</title>', exp_content)
exp_content = re.sub(r'<span class="current">Interior Design</span>', '<span class="current">Experience</span>', exp_content)
exp_content = re.sub(r'Interior <span class="gold-text">Designs</span>', 'Our <span class="gold-text">Experience</span>', exp_content)
exp_content = re.sub(r'Luxury living rooms, modular kitchens, office cabins, hotel suites - crafted with precision and passion.', 'Take a look at our completed projects and real estate journey through these videos.', exp_content)

# Remove filters bar
exp_content = re.sub(r'<div class="filters-bar.*?</div>', '', exp_content, flags=re.DOTALL)

# Replace gallery section with video grid
video_grid = """
<!-- Videos -->
<section class="gallery-section">
  <div class="container">
    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; justify-items: center; align-items: center;">
      <div style="width:100%; border-radius:16px; overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid var(--border-glass);">
        <iframe width="100%" height="315" src="https://www.youtube.com/embed/F9Dx3Y_MCVk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
      </div>
      <div style="width:100%; border-radius:16px; overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid var(--border-glass); max-width: 315px;">
        <iframe width="100%" height="560" src="https://www.youtube.com/embed/XEBCHrn0vY4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
      </div>
      <div style="width:100%; border-radius:16px; overflow:hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid var(--border-glass); max-width: 400px; display: flex; justify-content: center; background: #fff;">
        <iframe src="https://www.instagram.com/p/DXWrUx9thba/embed" width="100%" height="560" frameborder="0" scrolling="no" allowtransparency="true" style="background: white;"></iframe>
      </div>
    </div>
  </div>
</section>
"""

exp_content = re.sub(r'<!-- Gallery -->.*?<!-- Lightbox -->', video_grid + '\n<!-- Lightbox -->', exp_content, flags=re.DOTALL)

# Remove the JS for gallery
exp_content = re.sub(r'/\* ==============================\s+INTERIORS PAGE - GALLERY LOGIC\s+============================== \*/.*', '</script>\n</body>\n</html>', exp_content, flags=re.DOTALL)

# Fix the active state in navbar
exp_content = re.sub(r'<li><a href="interiors.html" style="color:var\(--gold\);">Interiors</a></li>', '<li><a href="interiors.html">Interiors</a></li>', exp_content)
exp_content = re.sub(r'<a href="interiors.html" style="color:var\(--gold\);">Interiors</a>', '<a href="interiors.html">Interiors</a>', exp_content)

with open('experience.html', 'w', encoding='utf-8') as f:
    f.write(exp_content)

# 2. Add Experience to navbars of all HTML files
html_files = glob.glob('*.html')
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Desktop nav
    if '<li><a href="experience.html"' not in content:
        content = re.sub(r'(<li><a href="ventures.html">Ventures</a></li>)', r'\1\n        <li><a href="experience.html">Experience</a></li>', content)
        content = re.sub(r'(<li><a href="ventures.html" style="color:var\(--gold\);">Ventures</a></li>)', r'\1\n        <li><a href="experience.html">Experience</a></li>', content)
        
        # In case the exact indentation/spacing is different
        content = re.sub(r'<li><a href="ventures\.html"(.*?)>Ventures</a></li>', r'<li><a href="ventures.html"\1>Ventures</a></li>\n        <li><a href="experience.html">Experience</a></li>', content)
        
    # Mobile nav
    if '<a href="experience.html"' not in content:
        content = re.sub(r'(<a href="ventures.html">Ventures</a>)', r'\1\n    <a href="experience.html">Experience</a>', content)
        content = re.sub(r'(<a href="ventures.html" style="color:var\(--gold\);">Ventures</a>)', r'\1\n    <a href="experience.html">Experience</a>', content)

    # Set active for experience.html
    if file == 'experience.html':
        content = re.sub(r'<li><a href="experience.html">Experience</a></li>', '<li><a href="experience.html" style="color:var(--gold);">Experience</a></li>', content)
        content = re.sub(r'<a href="experience.html">Experience</a>', '<a href="experience.html" style="color:var(--gold);">Experience</a>', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done")
