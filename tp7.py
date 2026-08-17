import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('cablecar.bmp',0)

#Transforme an image
dct = cv2.dct(np.float32(image))

#Show the DCT image
dctShow = np.log(1 + np.abs(dct))

#DCT inverse
image2 = cv2.idct(dct)
image2 = np.uint8(image2)

plt.figure(figsize=(10,4))
plt.subplot(1,3,1)
plt.title("Original")
plt.imshow(image, cmap='gray')

plt.subplot(1,3,2)
plt.title("DCT")
plt.imshow(dctShow, cmap='gray')

plt.subplot(1,3,3)
plt.title("resultat finale")
plt.imshow(image2, cmap='gray')

plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt


def jpeg_compress_decompress(img, fq):
   
    h, w = img.shape

    # ── Étape 1 : Padding pour que h et w soient multiples de 8 ──────────────
    haut  = 0
    bas   = (8 - h % 8) % 8
    gauche = 0
    droite = (8 - w % 8) % 8

    padImg = np.pad(img, ((haut, bas), (gauche, droite)), 'constant')
    pH, pW = padImg.shape

    # ── Étape 3 : Matrice de quantification 8×8 ───────────────────────────────
    Quant = np.fromfunction(lambda i, j: 1 + (1 + i + j) * fq, (8, 8), dtype=int)

    # Tableau de travail pour les blocs quantifiés
    dctImg    = np.zeros_like(padImg, dtype=np.float32)
    quantImg  = np.zeros_like(padImg, dtype=np.float32)
    reconImg  = np.zeros_like(padImg, dtype=np.float32)

    # ── Étapes 2-5 : Parcours bloc par bloc ──────────────────────────────────
    for i in range(0, pH, 8):
        for j in range(0, pW, 8):
            bloc = np.float32(padImg[i:i+8, j:j+8])

            # DCT du bloc
            dctBloc = cv2.dct(bloc)

            # Quantification (division entière)
            quantBloc = np.floor(dctBloc / Quant)

            # Dé-quantification
            dequantBloc = quantBloc * Quant

            # DCT inverse
            idctBloc = cv2.idct(dequantBloc)

            dctImg[i:i+8, j:j+8]   = dctBloc
            quantImg[i:i+8, j:j+8] = quantBloc
            reconImg[i:i+8, j:j+8] = idctBloc

    # ── Étape 6 : Suppression du padding et conversion uint8 ─────────────────
    result = reconImg[:h, :w]
    result = np.uint8(np.clip(result, 0, 255))
    return result

image = cv2.imread('cablecar.bmp', 0)

if image is None:
    image = cv2.imread(cv2.samples.findFile('lena.jpg'), 0)

if image is None:
    # Image synthétique de secours
    image = np.uint8(np.random.randint(0, 256, (240, 320)))

print(f"Image chargée : {image.shape[1]}×{image.shape[0]} pixels")

facteurs = [1, 5, 10, 25, 500]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

# Image originale dans la 1ère case
axes[0].imshow(image, cmap='gray')
axes[0].set_title('Image originale', fontsize=12, fontweight='bold')
axes[0].axis('off')

# Une case par facteur de quantification
for k, fq in enumerate(facteurs):
    result = jpeg_compress_decompress(image, fq)

    # PSNR pour évaluer la qualité
    mse  = np.mean((image.astype(np.float64) - result.astype(np.float64)) ** 2)
    psnr = 10 * np.log10(255**2 / mse) if mse > 0 else float('inf')

    axes[k + 1].imshow(result, cmap='gray')
    axes[k + 1].set_title(f'fq = {fq}  |  PSNR = {psnr:.1f} dB', fontsize=11)
    axes[k + 1].axis('off')

    print(f"fq={fq:3d}  →  PSNR = {psnr:.2f} dB")

plt.suptitle('Compression JPEG simplifiée — DCT 8×8 + Quantification', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('tp7_partie2_jpeg.png', dpi=150, bbox_inches='tight')
plt.show()