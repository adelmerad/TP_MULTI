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
