# %%
import numpy as np

import pytesseract
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


def tesseract_read(im, method='otsu'):
    grey = to_greyscale(np.asarray(im, dtype='float32'))/255
    plt_gray(grey)
    plt.show()

    thresh = simple_thresh(grey, method)

    binarized = binarize(grey, thresh)
    plt_gray(binarized)
    plt.show()

    text = pytesseract.image_to_string(binarized, lang='pol').lower()
    return text


def join_read(read_by_tesseract):
    return('\n'.join(read_by_tesseract.lower().split()))


def compare_methods(im):
    print("UNPROCESSED", '\n',
          join_read(pytesseract.image_to_string(im, lang='pol')))
    for i in (
        # 'median',
        # 'mean',
        'otsu',
        # 'li',
    ):
        print('\t', i, '\n', join_read(tesseract_read(im, i)))


if __name__ == '__main__':
    for im in load_images(15):
        compare_methods(im)

    print('\n===================\n')

    fb = Firebase.getInstance()
    fbarr = 3*[Firebase.getInstance()]
    storage = fb.storage

    test_img_path = 'images/test/test[1].jpg'
    output_path = os.path.join('images', 'test.jpg')
    storage.child(test_img_path).download(output_path)
    newim = Image.open(output_path)
    compare_methods(newim)
# %%
