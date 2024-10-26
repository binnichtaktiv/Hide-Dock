import os
import tempfile
import urllib.request
from PIL import Image

phoneAppearance = input("Which dark mode do you have activated?\n(1) normal dark mode\n(2) dark mode with dark icons\n")
base_image_path = input("Enter the path to the new image here where you want to hide the dock:\n")

base_image = Image.open(base_image_path)

normalDarkDock = "https://github.com/binnichtaktiv/Hide-Dock/blob/main/normalDarkDock.PNG?raw=true"
darkIconDarkModeDock = "https://github.com/binnichtaktiv/Hide-Dock/blob/main/darkIconDarkModeDock.png?raw=true"

if phoneAppearance == '1':
    imageUrl = normalDarkDock
else:
    imageUrl = darkIconDarkModeDock
    
with urllib.request.urlopen(imageUrl) as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(response.read())
        temp_path = tmp_file.name

overlay_image = Image.open(temp_path)

overlay_image = overlay_image.resize(base_image.size, Image.LANCZOS)

combined_image = Image.alpha_composite(base_image.convert('RGBA'), overlay_image.convert('RGBA'))

base_name, ext = os.path.splitext(base_image_path)
output_image_path = f"{base_name}_hiddenDock{ext}"

combined_image.save(output_image_path, 'PNG')
print("Your new background picture with hidden dock should be here: " + output_image_path)

os.unlink(temp_path)
