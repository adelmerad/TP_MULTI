import cv2
import numpy as np
import os


def encode_rle(image):

    pixels = image.flatten()
    encoded = []
    count = 1

    for i in range(1, len(pixels)):

        if pixels[i] == pixels[i-1] and count < 9:
            count += 1
        else:
            encoded.append((count, pixels[i-1]))
            count = 1

    encoded.append((count, pixels[-1]))

    return encoded


def decode_rle(encoded, height, width):

    resultat = []

    for count, value in encoded:
        for i in range(count):
            resultat.append(value)

    decoded_image = np.array(resultat).reshape((height, width)).astype(np.uint8)

    return decoded_image


output_folder = "decoded_TP5"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


image = cv2.imread("Image.bmp", 0)

h, w = image.shape

encoded = encode_rle(image)

decoded = decode_rle(encoded, h, w)

original_bits = image.size * 8
encoded_bits = len(encoded) * 16
ratio = (encoded_bits / original_bits) * 100

save_path = os.path.join(output_folder, "decoded_image.bmp")
cv2.imwrite(save_path, decoded)

print("\n[ENCODE] Image.bmp")
print("Original :", original_bits, "bits")
print("Encoded  :", encoded_bits, "bits")
print("Ratio    :", round(ratio,2), "%")
print("Saved ->", os.path.abspath(save_path))


cv2.imshow("Original image", image)
cv2.imshow("Decoded image", decoded)


image2 = cv2.imread("cablecar.bmp", 0)

h2, w2 = image2.shape

encoded2 = encode_rle(image2)

decoded2 = decode_rle(encoded2, h2, w2)

original_bits2 = image2.size * 8
encoded_bits2 = len(encoded2) * 16
ratio2 = (encoded_bits2 / original_bits2) * 100

save_path2 = os.path.join(output_folder, "decoded_cablecar.bmp")
cv2.imwrite(save_path2, decoded2)

print("\n[ENCODE] cablecar.bmp")
print("Original :", original_bits2, "bits")
print("Encoded  :", encoded_bits2, "bits")
print("Ratio    :", round(ratio2,2), "%")
print("Saved ->", os.path.abspath(save_path2))

cv2.imshow("Original cablecar", image2)
cv2.imshow("Decoded cablecar", decoded2)


cv2.waitKey(0)
cv2.destroyAllWindows()