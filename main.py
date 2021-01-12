# %%
import numpy as np
import pytesseract
# import cv2
import os
from PIL import Image
# import argparse
from matplotlib import pyplot as plt

from connectivity import Firebase
from image_manipulation import (
    load_images,
    to_greyscale,
    simple_thresh,
    binarize,
    plt_gray,
    )


def tesseract_read(im):
    grey = to_greyscale(np.asarray(im, dtype='float32'))/255
    plt_gray(grey)
    plt.show()

    thresh = simple_thresh(grey, 'otsu')
    print(thresh)

    binarized = binarize(grey, thresh)
    plt_gray(binarized)
    plt.show()

    text = pytesseract.image_to_string(binarized, lang='pol')
    return text


if __name__ == '__main__':
    for im in load_images(15):
        print(tesseract_read(im).split())
    print('\n\n\n')
    fb = Firebase.getInstance()
    fbarr = 3*[Firebase.getInstance()]
    storage = fb.storage

    test_img_path = 'images/test/test[1].jpg'
    output_path = os.path.join('images', 'test.jpg')
    storage.child(test_img_path).download(output_path)
    newim = Image.open(output_path)
    plt_gray(newim)
    plt.show()
    tesseract_read(newim)
# %%
