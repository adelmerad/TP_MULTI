import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the image 
img = cv2.imread('cablecar.bmp') 
if img is None:  
    print("Erreur : Impossible de charger l'image.")  
else:  
        print (type(img)) 
        # Get the image height and width 
        height, width, channels = img.shape 
        print (f'height: {height} / width: {width} / channels: {channels}') 
        # Create a window with a title "Image" to display the image 
        cv2.imshow("Image", img) 
        # Hold the screen until the user closes it. 
        cv2.waitKey(0) 
        # Destroy the window 
        cv2.destroyAllWindows()

# Resize an image  
resized_img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2))) 
# Save the image  
cv2.imwrite("resized.png", resized_img)

import numpy as np

# Convert from BGR to YCrCb color space: Y is the Luminance component, Cb and Cr chrominance components  
img_ycrcb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2YCrCb) 
cv2.imwrite("ycrcb_random.png", img_ycrcb) 
# Convert from BGR to HSV color space 
img_hsv = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV) 
cv2.imwrite("hsv_random.png", img_hsv) 
# Convert an RGB image to grayscale 
img_gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY) 
# concatenate image Horizontally 
images = np.concatenate((cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR), img_ycrcb, img_hsv), axis=1)   
cv2.imshow('Gray, YCrCb and HSV images', images) 
cv2.waitKey(0) 
cv2.destroyAllWindows()

import matplotlib.pyplot as plt  
# Read the image with OpenCV 
 
# Converting BGR color to RGB color format 
RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
 
# Display the image using plt 
plt.imshow(RGB_img) 
# Show without the axes 
plt.axis('off') 
# Put a title 
plt.title('Image') 
plt.show()

# %% 
# Separate and merge RGB images 
B, G, R = cv2.split(img) 
RGB_img = cv2.merge([R, G, B]) 

plt.imshow(RGB_img) 
plt.axis('off') 
plt.title('Image') 
plt.show()

# %% 
# création d’images vide de la même forme que l’image d’origine 
R_img = np.zeros_like(img) 
G_img = np.zeros_like(img) 
B_img = np.zeros_like(img) 
 
# assigner la valeur de chaque canal a la composante correspondante en laissant les autres canaux a 0 
R_img[:, :, 0] = R  # Canal Rouge 
G_img[:, :, 1] = G  # Canal Vert 
B_img[:, :, 2] = B  # Canal Bleu 
 
figure, plot = plt.subplots(nrows=1, ncols=3) 
 
plot[0].imshow(R_img) 
plot[0].set_title('canal rouge') 
plot[0].axis('off') 
 
plot[1].imshow(G_img) 
plot[1].set_title('canal vert') 
plot[1].axis('off') 
 
plot[2].imshow(B_img) 
plot[2].set_title('canal bleu') 
plot[2].axis('off') 
    
plt.show() 