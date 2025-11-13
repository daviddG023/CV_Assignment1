import math
import numpy as np
from integralImage import doubleIntegral
from PIL import Image
import matplotlib.pyplot as plt
from detectEyes import DetectEye, ExtractDetectedEye
from readImage import readImage

if __name__ == "__main__":
    i=7
    pathAndSizeKernal = [("Image 1.jpeg", 330), ("Image 2.jpeg", 250), 
    ("Image 3.jpeg", 150), ("Image 4.jpeg", 150), ("Image 5.jpeg",90),
    ("Image 6.jpeg", 160), ("Image 7.jpeg", 170), 
    ("Image 8.jpeg", 220)]
    path = "Images/"
    img_path = path + pathAndSizeKernal[i][0]
    n = pathAndSizeKernal[i][1]
    img = readImage(img_path)

    I = doubleIntegral(img)
    center = DetectEye(I, n)

    masked, bbox = ExtractDetectedEye(img, center, n)
    print("Center:", center, "BBox (top,left,bottom,right):", bbox)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(img, cmap='gray'); axes[0].scatter([center[1]], [center[0]], s=80)
    axes[0].set_title("Original + detected center"); axes[0].axis('off')
    axes[1].imshow(masked, cmap='gray'); axes[1].set_title(f"Extracted eye area (n={n})"); axes[1].axis('off')
    plt.show()
