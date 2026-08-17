import cv2
import numpy as np
import matplotlib.pyplot as plt

gray_img = cv2.imread("cablecar.bmp", cv2.IMREAD_GRAYSCALE)

if gray_img is None:
    print("Erreur : image introuvable")
else:
    print("Image chargée avec succès")

kernel1 = np.ones((5, 5), np.float32) / 30


kernel2 = np.array([[-1,-1,-1],
                    [-1, 8,-1],
                    [-1,-1,-1]])

conv1 = cv2.filter2D(gray_img, -1, kernel1)  
conv2 = cv2.filter2D(gray_img, -1, kernel2)  

plt.subplot(1,3,1), plt.imshow(gray_img, cmap="gray"), plt.title("Original")
plt.subplot(1,3,2), plt.imshow(conv1, cmap="gray"), plt.title("Flou")
plt.subplot(1,3,3), plt.imshow(conv2, cmap="gray"), plt.title("Contours")
plt.show()



def convolution(pad_img, kernel):
    p = kernel.shape[0] // 2   
    pheight, pwidth = pad_img.shape
    img_conv = np.zeros(pad_img.shape)

    for i in range(p, pheight - p):
        for j in range(p, pwidth - p):
            roi = pad_img[i-p:i+p+1, j-p:j+p+1]   
            img_conv[i, j] = np.sum(kernel * roi)

    return img_conv[p:-p, p:-p]

gray_img = cv2.imread("cablecar.bmp", cv2.IMREAD_GRAYSCALE)


kernel = np.array([[-1,-1,-1],
                   [-1, 8,-1],
                   [-1,-1,-1]])

p = kernel.shape[0] // 2
pad_img = np.zeros((gray_img.shape[0] + 2*p, gray_img.shape[1] + 2*p))
pad_img[p:-p, p:-p] = gray_img

conv_opencv = cv2.filter2D(gray_img, -1, kernel)

conv_manual = convolution(pad_img, kernel)

plt.subplot(1,2,1), plt.imshow(conv_opencv, cmap="gray"), plt.title("cv2.filter2D")
plt.subplot(1,2,2), plt.imshow(conv_manual, cmap="gray"), plt.title("Convolution manuelle")
plt.show()


kernels = [
    np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),   
    np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]),       
    np.array([[-1,0,1],[-2,0,2],[-1,0,1]]),        
    np.array([[-1,1,1],[0,-2,-1],[0,1,2]]),       
    np.array([[1,1,2],[2,4,2],[1,1,2]]) / 16      
]

img = cv2.imread("cablecar.bmp")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray_img.shape
h_block, w_block = h // 4, w // 4

blocks = []
for i in range(4):
    for j in range(4):
        block = gray_img[i*h_block:(i+1)*h_block, j*w_block:(j+1)*w_block]
        
        kernel = kernels[np.random.randint(len(kernels))]
        
        filtered_block = cv2.filter2D(block, -1, kernel)
        blocks.append(filtered_block)
rows = []
for i in range(4):
    row = np.hstack(blocks[i*4:(i+1)*4])
    rows.append(row)
final_img = np.vstack(rows)


plt.imshow(final_img, cmap="gray")
plt.title("Image filtrée en 16 blocs")
plt.show()