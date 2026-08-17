# adel merad 222231658203

import cv2
import numpy as np

image = cv2.imread("Image.bmp", cv2.IMREAD_GRAYSCALE)

_, binary = cv2.threshold(image, 127, 1, cv2.THRESH_BINARY)

fimage = binary.flatten()

rle = []

count = 1
current = fimage[0]

for pixel in fimage[1:]:
    
    if pixel == current:
        count += 1
    else:
        rle.append((count, current))
        current = pixel
        count = 1

rle.append((count, current))

encoded = ""

for count, value in rle:
    
    valeur = "{:03}".format(count)
    
    encoded += valeur + str(value)

file_name = "compressed.txt"

with open(file_name, "w") as file:
    file.write(encoded)

with open(file_name, "r") as file:
    txt = file.readlines()[0]

print("Chaine compressée : ")
print(txt)

taille_image = binary.size
taille_bits_image = taille_image

taille_code = len(encoded)

taux = (taille_code / taille_bits_image) * 100

print("Taille image :", taille_bits_image, "bits")
print("Taille code :", taille_code, "bits")
print("Taux de compression :", taux, "%")