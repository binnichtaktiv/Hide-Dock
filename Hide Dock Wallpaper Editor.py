import os
import tempfile
import urllib.request
from PIL import Image

base_image_path = input("Enter the path to the new image here where you want to hide the dock:\n")

base_image = Image.open(base_image_path)

overlay_image_url = "https://github.com/binnichtaktiv/Hide-Dock-Wallpaper-Editor/blob/main/Dock.PNG?raw=true"
with urllib.request.urlopen(overlay_image_url) as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(response.read())
        temp_path = tmp_file.name

overlay_image = Image.open(temp_path)

overlay_image = overlay_image.resize(base_image.size, Image.LANCZOS)

combined_image = Image.alpha_composite(base_image.convert('RGBA'), overlay_image.convert('RGBA'))

base_name, ext = os.path.splitext(base_image_path)
output_image_path = f"{base_name}_hiddenDock{ext}"

combined_image.save(output_image_path, 'PNG')
print("Your new background picture with hidden dock should be here:" + output_image_path)

os.unlink(temp_path)
