import numpy as np
import matplotlib.pyplot as plt
import cv2

# ============================================================
# PARTIE 1 : Vecteur de mouvement sur bloc 2x2 (exemple TP)
# ============================================================

bloc_courant = np.array([[10, 12],
                          [14, 16]], dtype=np.float32)

zone_recherche = np.array([[10, 11, 12, 13],
                            [14, 15, 16, 17],
                            [18, 19, 20, 21],
                            [22, 23, 24, 25]], dtype=np.float32)

N = 2  # taille du bloc
H, W = zone_recherche.shape
best_mse = float('inf')
best_pos = (0, 0)

print("=" * 40)
print("PARTIE 1 - Blocs candidats 2x2")
print("=" * 40)

for dy in range(H - N + 1):         
    for dx in range(W - N + 1):     
        # Extraire le bloc candidat
        candidat = zone_recherche[dy:dy+N, dx:dx+N]
        
        # Calculer le MSE
        mse = np.mean((bloc_courant - candidat) ** 2)
        
        print(f"Position ({dy},{dx}) → bloc = {candidat.tolist()} → MSE = {mse:.2f}")
        
        if mse < best_mse:
            best_mse = mse
            best_pos = (dy, dx)

dy_best, dx_best = best_pos
meilleur_bloc = zone_recherche[dy_best:dy_best+N, dx_best:dx_best+N]
residu = bloc_courant - meilleur_bloc

print(f"\n Meilleur bloc à la position (dy={dy_best}, dx={dx_best}) avec MSE = {best_mse:.2f}")
print(f"   Vecteur de mouvement : (dx={dx_best}, dy={dy_best})")
print(f"   Meilleur bloc :\n{meilleur_bloc}")
print(f"   Résidu (courant - meilleur) :\n{residu}")

# ============================================================
# PARTIE 2 : Application sur de vraies images
# ============================================================

# --- Chargement des images en niveaux de gris ---
img1 = cv2.imread("frame_1.png", cv2.IMREAD_GRAYSCALE).astype(np.float32)
img2 = cv2.imread("frame_2.png", cv2.IMREAD_GRAYSCALE).astype(np.float32)

# Vérification que les deux images ont la même taille
assert img1.shape == img2.shape, "Les deux images doivent avoir la même taille"

H, W = img2.shape
BLOCK = 16       # taille des blocs (16x16)
SEARCH = 4       # zone de recherche ±4 pixels

# Listes pour stocker les vecteurs de mouvement
xs, ys = [], []        # centres des blocs (pour quiver)
dxs, dys = [], []      # vecteurs de mouvement

# Image résidu (même taille que img2)
residus_image = np.zeros_like(img2)

print("\n" + "=" * 40)
print("PARTIE 2 - Vecteurs de mouvement 16x16")
print("=" * 40)

# --- Parcourir img2 bloc par bloc ---
for y in range(0, H - BLOCK + 1, BLOCK):       # lignes
    for x in range(0, W - BLOCK + 1, BLOCK):   # colonnes
        
        # Bloc courant dans img2
        bloc_courant_2 = img2[y:y+BLOCK, x:x+BLOCK]
        
        best_mse = float('inf')
        best_dx, best_dy = 0, 0
        
        # --- Zone de recherche dans img1 (±4 pixels) ---
        for dy in range(-SEARCH, SEARCH + 1):
            for dx in range(-SEARCH, SEARCH + 1):
                # Position candidate dans img1
                ny = y + dy
                nx = x + dx
                
                # Vérifier que le bloc reste dans les limites de img1
                if ny < 0 or nx < 0 or ny + BLOCK > H or nx + BLOCK > W:
                    continue
                
                # Bloc candidat dans img1
                candidat_1 = img1[ny:ny+BLOCK, nx:nx+BLOCK]
                
                # MSE entre bloc courant et candidat
                mse = np.mean((bloc_courant_2 - candidat_1) ** 2)
                
                if mse < best_mse:
                    best_mse = mse
                    best_dx, best_dy = dx, dy
        
        # --- Meilleur bloc trouvé ---
        ny_best = y + best_dy
        nx_best = x + best_dx
        meilleur = img1[ny_best:ny_best+BLOCK, nx_best:nx_best+BLOCK]
        
        # --- Résidu ---
        residu_bloc = bloc_courant_2 - meilleur
        residus_image[y:y+BLOCK, x:x+BLOCK] = residu_bloc
        
        # Affichage du résidu avec print (demandé par le TP)
        print(f"Bloc ({y},{x}) → vecteur=({best_dx},{best_dy}), MSE={best_mse:.2f}")
        print(f"Résidu :\n{residu_bloc.astype(int)}\n")
        
        # Centre du bloc pour quiver
        xs.append(x + BLOCK // 2)
        ys.append(y + BLOCK // 2)
        dxs.append(best_dx)
        dys.append(best_dy)

# ============================================================
# VISUALISATION
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Image 1 - référence
axes[0].imshow(img1, cmap='gray')
axes[0].set_title("Image de référence (img1)")
axes[0].axis('off')

# Image 2 avec vecteurs de mouvement
axes[1].imshow(img2, cmap='gray')
axes[1].quiver(xs, ys, dxs, dys,
               color='red', angles='xy', scale_units='xy',
               scale=1, width=0.003)
axes[1].set_title("img2 + Vecteurs de mouvement")
axes[1].axis('off')

# # Image résidu
im = axes[2].imshow(residus_image, cmap='RdBu', vmin=-50, vmax=50)
axes[2].set_title("Image résidu (img2 − meilleur bloc img1)")
plt.colorbar(im, ax=axes[2])
axes[2].axis('off')

plt.tight_layout()
plt.savefig("resultat_tp8.png", dpi=150)
plt.show()
print("Figure sauvegardée : resultat_tp8.png")