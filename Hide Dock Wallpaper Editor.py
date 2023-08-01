import cv2
import numpy as np
import requests
import tempfile

# Farbe definieren
color = np.uint8([[[36, 36, 36]]]) # RGB-Wert von #242424
tolerance = 20  # Toleranz für Farbauswahl

lower_color = np.clip(color - tolerance, 0, 255)
upper_color = np.clip(color + tolerance, 0, 255)

# URL des ursprünglichen Bildes
original_image_url = 'https://hostigram.xyz/?tkn=7HYuqMs1vTgcW7OTQIDI2XpCqsuPRvMrRoVIyjb1TBKgo&dl=1'

print("Downloading original image...")
# Bild herunterladen
response = requests.get(original_image_url, stream=True)
response.raise_for_status()
with tempfile.NamedTemporaryFile(delete=True) as fp:
    fp.write(response.content)
    original_image_path = fp.name

    print("Download complete. Processing image...")
    # Bild laden
    img = cv2.imread(original_image_path)

    # Proportion des unteren Teils des Bildes, der betrachtet werden soll
    proportion = 0.3
    crop_img = img[int(img.shape[0]*(1-proportion)):, :]

    # Bereich mit der Farbe finden
    mask = cv2.inRange(crop_img, lower_color, upper_color)

    # Bereich ausschneiden
    cutout = cv2.bitwise_and(crop_img, crop_img, mask=mask)

    # Pfad zum neuen Bild
    new_image_path = input("Enter the path to the new image here where you want to hide the dock:\n")

    # Pfad zum Ausgabebild
    output_image_path = input("Enter path to output folder here:\n")
    output_image_path = output_image_path + "/modified.png"
    # Neues Bild laden
    new_img = cv2.imread(new_image_path)

    # Unteren Teil des neuen Bildes schneiden
    new_img_crop = new_img[int(new_img.shape[0]*(1-proportion)):, :]

    # Skalieren des ausgeschnittenen Bereichs auf die Größe des neuen Bildes
    cutout = cv2.resize(cutout, (new_img_crop.shape[1], new_img_crop.shape[0]))

    # Skalieren der Maske auf die Größe des neuen Bildes
    mask = cv2.resize(mask, (new_img_crop.shape[1], new_img_crop.shape[0]))

    # Bereich auf neues Bild übertragen
    new_img_crop[mask != 0] = cutout[mask != 0]

    # Den unteren Teil des neuen Bildes ersetzen
    new_img[int(new_img.shape[0]*(1-proportion)):, :] = new_img_crop

    # Bild speichern
    if cv2.imwrite(output_image_path, new_img):
        print(f"Image saved to {output_image_path}")
    else:
        print(f"Failed to save image to {output_image_path}")
