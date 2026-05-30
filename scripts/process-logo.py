"""Compress logo.png and create favicon.ico"""
from PIL import Image
import os

src = r"F:\Coding\teamthrow.online\logo.png"
dst_dir = r"F:\Coding\teamthrow.online"

img = Image.open(src)
print(f"Original: {img.size}, mode={img.mode}")

# --- Resize for nav bar (fit within 60px nav height) ---
aspect = img.width / img.height
nav_height = 52
nav_width = int(nav_height * aspect)
nav_img = img.resize((nav_width, nav_height), Image.LANCZOS)
nav_path = os.path.join(dst_dir, "logo-nav.png")
nav_img.save(nav_path, "PNG", optimize=True)
print(f"Nav logo: {nav_img.size} -> {os.path.getsize(nav_path) / 1024:.1f}KB")

# --- Create favicon.ico (32x32 + 16x16) ---
fav32 = img.resize((32, 32), Image.LANCZOS)
fav16 = img.resize((16, 16), Image.LANCZOS)
ico_path = os.path.join(dst_dir, "favicon.ico")
fav32.save(ico_path, "ICO", sizes=[(32, 32), (16, 16)])
print(f"Favicon: {os.path.getsize(ico_path) / 1024:.1f}KB")

# --- Also compress the original for web use ---
# Resize to max 400px width for the site (it's used in nav/footer)
web_width = 400
web_height = int(web_width / aspect)
web_img = img.resize((web_width, web_height), Image.LANZZOS if hasattr(Image, 'LANZZOS') else Image.LANCZOS)
web_path = os.path.join(dst_dir, "logo-web.png")
web_img.save(web_path, "PNG", optimize=True)
print(f"Web logo: {web_img.size} -> {os.path.getsize(web_path) / 1024:.1f}KB")

print("\nDone! Files created:")
print(f"  logo-nav.png  - nav bar logo (52px tall)")
print(f"  logo-web.png  - compressed web version (400px wide)")
print(f"  favicon.ico   - browser tab icon (32+16px)")
