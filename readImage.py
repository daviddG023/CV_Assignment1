import numpy as np
from PIL import Image


def readImage(image_path):
    img = Image.open(image_path).convert("L")
    return np.array(img)
