# LZW Compression
def lzw_compress(data):
    # Initialize dictionary with all 256 ASCII characters
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    codes = []
    w = ""

    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc  # extend current string
        else:
            codes.append(dictionary[w])   # output code for w
            dictionary[wc] = next_code    # add w+c to dictionary
            next_code += 1
            w = c                         # reset to current char

    if w:
        codes.append(dictionary[w])  # flush last code

    return codes, dictionary

# Example
data = "ABABABA"
codes, dico = lzw_compress(data)
print("Codes:", codes)

# Compression rate
original_bits = len(data) * 8
import math
bits_per_code = math.ceil(math.log2(max(codes) + 1))
compressed_bits = len(codes) * bits_per_code
rate = original_bits / compressed_bits
print(f"Taux de compression: {rate:.2f}x")

import numpy as np
from PIL import Image
import math

# Read grayscale image
img = Image.open("cablecar.bmp").convert("L")
data = np.array(img).flatten()

# Convert pixel values to characters
data_str = "".join([chr(p) for p in data]) 

# Compress
codes, _ = lzw_compress(data_str)

# Compute compression ratio
original_bits = len(data_str) * 8
bits_per_code = math.ceil(math.log2(max(codes) + 1))
compressed_bits = len(codes) * bits_per_code
print(f"Image size    : {img.size}")
print(f"Original bits : {original_bits}")
print(f"Compressed    : {compressed_bits}")
print(f"Ratio         : {original_bits/compressed_bits:.2f}x")