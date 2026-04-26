import os
import glob
import re

html_files = glob.glob('c:/Users/srini/Downloads/madhavi enterprises/frontend/*.html')

top_bar_html = """
  <!-- ===== TOP BAR ===== -->
  <div class="top-bar">
    <div class="container">
      <div class="top-bar-contact">
        <a href="tel:+919666313007"><i class="fa-solid fa-phone"></i> +91 96663 13007</a>
        <a href="mailto:dasamrao@gmail.com"><i class="fa-solid fa-envelope"></i> dasamrao@gmail.com</a>
      </div>
      <div class="top-bar-socials">
        <a href="#"><i class="fa-brands fa-youtube"></i></a>
        <a href="#"><i class="fa-brands fa-facebook"></i></a>
        <a href="#"><i class="fa-brands fa-instagram"></i></a>
        <a href="#"><i class="fa-brands fa-linkedin"></i></a>
      </div>
    </div>
  </div>
"""

side_btns_html = """
  <!-- ===== FLOATING SIDE BUTTONS ===== -->
  <div class="floating-side-group fade-in-up">
    <a href="https://wa.me/919666313007" target="_blank" class="side-btn wa" aria-label="WhatsApp">
      <i class="fa-brands fa-whatsapp"></i>
    </a>
    <a href="tel:+919666313007" class="side-btn call" aria-label="Call">
      <i class="fa-solid fa-phone"></i>
    </a>
    <button class="side-btn-quote" onclick="openLeadModal('Get Free Estimation','','')">
      Get Quote
    </button>
  </div>
"""

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add top bar before navbar if not exists
    if 'class="top-bar"' not in content:
        content = re.sub(r'(<nav class="navbar")', r'{}\n  \1'.format(top_bar_html), content)

    # 2. Add Get Free Estimation button to navbar if not exists
    if 'btn-estimation' not in content:
        # We find the nav-links </ul> and append the button right after it, but inside the nav-inner
        # Or add it as a new li. Let's add it as a new li.
        estimation_btn = '<li><a href="#" class="btn-estimation" onclick="openLeadModal(\\\'Get Free Estimation\\\',\\\'\\\',\\\'\\\')">Get Free Estimation</a></li>\n      </ul>'
        content = re.sub(r'</ul>', estimation_btn, content, count=1)

    # 3. Replace floating WA button with new side group
    if 'class="wa-float"' in content:
        # Regex to remove the old wa-float block
        content = re.sub(r'<!-- ===== FLOATING WA ===== -->.*?</a>', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- ===== FLOATING WA BUTTON ===== -->.*?</a>', '', content, flags=re.DOTALL)
        content = re.sub(r'<a href="[^"]*" target="_blank" class="wa-float".*?</a>', '', content, flags=re.DOTALL)
        
    if 'class="floating-side-group"' not in content:
        # Insert before closing body
        content = content.replace('</body>', side_btns_html + '\n</body>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

for f in html_files:
    update_file(f)
