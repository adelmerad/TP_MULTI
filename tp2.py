import cv2 
 
# Read the image 
img= cv2.imread('cablecar.bmp') 
 
if img is None:  
    print("Erreur : Impossible de charger l'image.")  
else:  
     # Get the image height and width 
    height, width, _ = img.shape 
for y in range(height):  
    for x in range(width): 
        pixel = img[y, x]  
        B, G, R = pixel 
        if 100 < x < 200 and 100 < y < 150 : 
            img[y, x] = (255,0,0) 
# Show the image
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Définir la taille des blocs 
block_size = int(width/2) 
# Parcourir l'image bloc par bloc 
for y in range(0, height, block_size):   
    for x in range(0, width, block_size): 
        # Définir les limites du bloc 
        y_end = min(y + block_size, height) 
        x_end = min(x + block_size, width) 
        # Extraire le bloc 
        block = img[y:y_end, x:x_end] 
        # Afficher les coordonnées du bloc 
        print(f"Bloc ({x}, {y}) → ({x_end}, {y_end})") 
        # Afficher chaque bloc 
        cv2.imshow("Bloc", block) 
        cv2.waitKey(1000)   
 
cv2.destroyAllWindows()