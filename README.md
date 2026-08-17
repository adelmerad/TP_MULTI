# TP Multimédia — Traitement d'images & Compression

Ensemble de travaux pratiques (TP1 à TP8) en Python autour de deux grands thèmes du traitement multimédia :

- **Traitement d'images numériques** avec OpenCV (espaces de couleur, filtrage/convolution, binarisation)
- **Compression de données** (RLE, LZW, DCT/JPEG) et **estimation de mouvement** vidéo

## Prérequis

```
pip install opencv-python numpy matplotlib pillow
```

Chaque script est indépendant et se lance directement :

```
python tp1.py
```

Les scripts qui affichent des fenêtres OpenCV (`cv2.imshow`) attendent une frappe clavier (`cv2.waitKey(0)`) pour passer à l'étape suivante.

## Fichiers d'entrée nécessaires

| Fichier | Utilisé par |
|---|---|
| `cablecar.bmp` | tp1, tp2, TP3, tp5, tp6, tp7 |
| `Image.bmp` | tp4, tp5 |
| `frame_1.png`, `frame_2.png` | tp8 (deux frames vidéo consécutives) |

✅ **Correction apportée** : `tp4.py` et `tp5.py` chargeaient initialement le fichier via le nom `image.bmp` (minuscules) alors que le fichier réel s'appelle `Image.bmp`. Ça fonctionnait par chance sur Windows (système de fichiers insensible à la casse) mais aurait planté sur Linux/macOS. Les deux scripts ont été corrigés pour utiliser `Image.bmp`.

## Détail des TP

### TP1 — Prise en main d'OpenCV (`tp1.py`)
Lecture d'une image BMP, affichage des dimensions (hauteur/largeur/canaux), redimensionnement (÷2) sauvegardé en `resized.png`. Conversions d'espaces colorimétriques BGR → **YCrCb** (`ycrcb_random.png`) et BGR → **HSV** (`hsv_random.png`), comparées côte à côte avec la version niveaux de gris. Affichage RGB via matplotlib, puis séparation/fusion des canaux **R, G, B** (`cv2.split`/`cv2.merge`) et visualisation de chaque canal isolé sur fond noir.

### TP2 — Manipulation de pixels et binarisation (`tp2.py`)
Parcours pixel par pixel pour colorier en rouge une zone rectangulaire de l'image. Découpage de l'image en blocs (moitié de la largeur) affichés un par un. Binarisation par **seuillage fixe** (127) comparée à la **méthode d'Otsu** (seuil calculé automatiquement), avec affichage comparatif.

### TP3 — Filtrage par convolution (`TP3.py`)
Application de deux filtres via `cv2.filter2D` : un flou (noyau moyenneur 5×5) et un détecteur de contours (noyau laplacien 3×3). **Implémentation manuelle de la convolution 2D** (avec padding) comparée au résultat `cv2.filter2D` pour vérifier l'équivalence. Enfin, découpage de l'image en une grille 4×4 (16 blocs) où un filtre est tiré aléatoirement parmi 5 noyaux (contours, netteté, Sobel-like, filtre personnalisé, flou gaussien-like) pour chaque bloc, puis recomposition de l'image finale.

### TP4 — Compression RLE simple (`tp4.py`)
Binarisation de l'image, puis **encodage RLE (Run-Length Encoding)** du flux de bits aplati : chaque run est encodé en un compteur sur 3 chiffres suivi de la valeur (0/1). Résultat sauvegardé dans `compressed.txt`. Calcul du **taux de compression** obtenu par rapport à la taille binaire originale.

### TP5 — Compression RLE bornée + décodage (`tp5.py`)
Variante du RLE avec un compteur borné à 9 (encodage sur 2 caractères), appliquée en niveaux de gris. Contrairement au TP4, ce script **décode** aussi les données pour reconstruire l'image (`decode_rle`) et sauvegarde le résultat dans `decoded_TP5/`. Comparaison taille originale vs compressée sur deux images (`Image.bmp` et `cablecar.bmp`), avec affichage original/décodé côte à côte.

### TP6 — Compression LZW (`tp6.py`)
Implémentation de l'algorithme **LZW (Lempel-Ziv-Welch)** avec dictionnaire adaptatif démarrant aux 256 caractères ASCII. Testé d'abord sur une chaîne simple (`"ABABABA"`), puis appliqué aux pixels d'une image en niveaux de gris (convertis en chaîne de caractères via `chr()`). Calcul du taux de compression en bits/code selon la taille du dictionnaire final.

### TP7 — Compression JPEG simplifiée / DCT (`tp7.py`)
**Partie 1** : transformée en cosinus discrète (**DCT**) globale de l'image via `cv2.dct`, visualisation du spectre fréquentiel (log-magnitude), puis reconstruction par **IDCT** inverse.
**Partie 2** : pipeline JPEG simplifié bloc par bloc (8×8) — padding pour que les dimensions soient multiples de 8, DCT par bloc, **quantification** avec une matrice croissante selon un facteur `fq`, déquantification, IDCT, reconstruction. Le **PSNR** est calculé pour chaque facteur de quantification testé (1, 5, 10, 25, 500) afin de visualiser le compromis qualité/compression. Résultat sauvegardé dans `tp7_partie2_jpeg.png`.

### TP8 — Estimation de mouvement (`tp8.py`)
**Partie 1** : exemple pédagogique — recherche du meilleur bloc 2×2 dans une zone 4×4 par minimisation du **MSE** (Mean Squared Error), calcul du vecteur de mouvement et du résidu (bloc courant − meilleur bloc trouvé).
**Partie 2** : application réelle sur deux frames vidéo consécutives (`frame_1.png` → `frame_2.png`). Découpage en blocs 16×16, recherche exhaustive dans une fenêtre de ±4 pixels autour de chaque bloc, calcul du vecteur de mouvement optimal et de l'image résidu. Visualisation finale avec les vecteurs de mouvement superposés (flèches `quiver`) et la carte des résidus, sauvegardée dans `resultat_tp8.png`.

## Résultats générés

Ces fichiers sont produits en exécutant les scripts (déjà présents dans le dépôt comme exemples de sortie) :

- `resized.png`, `ycrcb_random.png`, `hsv_random.png` — TP1
- `compressed.txt` — TP4
- `decoded_TP5/decoded_image.bmp`, `decoded_TP5/decoded_cablecar.bmp` — TP5
- `tp7_partie2_jpeg.png` — TP7
- `resultat_tp8.png` — TP8
