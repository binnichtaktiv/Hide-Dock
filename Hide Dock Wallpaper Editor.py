import cv2
import numpy as np
import requests
import tempfile
import os

color = np.uint8([[[36, 36, 36]]])
tolerance = 20
lower_color = np.clip(color - tolerance, 0, 255)
upper_color = np.clip(color + tolerance, 0, 255)
original_image_url = 'https://github.com/binnichtaktiv/Hide-Dock-Wallpaper-Editor/blob/main/Template.JPG?raw=true'

print("Downloading original image...")
response = requests.get(original_image_url, stream=True)
response.raise_for_status()
temp_dir = tempfile.mkdtemp()
original_image_path = os.path.join(temp_dir, 'temp_image.jpg')
with open(original_image_path, 'wb') as fp:
    fp.write(response.content)

print("Download complete. Processing image...")
img = cv2.imread(original_image_path)
proportion = 0.3
crop_img = img[int(img.shape[0]*(1-proportion)):, :]
mask = cv2.inRange(crop_img, lower_color, upper_color)
cutout = cv2.bitwise_and(crop_img, crop_img, mask=mask)
new_image_path = input("Enter the path to the new image here where you want to hide the dock:\n")
output_image_path = input("Enter path to output folder here:\n")
output_image_path = output_image_path + "/modified.png"
new_img = cv2.imread(new_image_path)
new_img_crop = new_img[int(new_img.shape[0]*(1-proportion)):, :]
cutout = cv2.resize(cutout, (new_img_crop.shape[1], new_img_crop.shape[0]))
mask = cv2.resize(mask, (new_img_crop.shape[1], new_img_crop.shape[0]))
new_img_crop[mask != 0] = cutout[mask != 0]
new_img[int(new_img.shape[0]*(1-proportion)):, :] = new_img_crop

if cv2.imwrite(output_image_path, new_img):
    print(f"Image saved to {output_image_path}")
else:
    print(f"Failed to save image to {output_image_path}")
