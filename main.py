# %%
import numpy as np
import pytesseract
import os
# from PIL import Image
# import argparse
import matplotlib as mpl
from matplotlib import pyplot as plt
from connectivity import Firebase
from image_manipulation import (
    # load_images,
    to_greyscale,
    simple_thresh,
    binarize,
    plt_gray,
    )
from regular_expressions import RegularExpressions

mpl.rcParams['figure.dpi'] = 300


def tesseract_read(im, method='otsu', lang="pol", is_plot=False):
    grey = to_greyscale(np.asarray(im, dtype='float32'))/255
    thresh = simple_thresh(grey, method)
    binarized = binarize(grey, thresh)
    if is_plot:
        plt_gray(grey)
        plt.show()
        plt_gray(binarized)
        # plt.savefig(f'{method}.pdf')
        plt.show()

    text = pytesseract.image_to_string(binarized, lang=lang)
    return text


def print_found(read_by_tesseract):
    re = RegularExpressions()
    for exp in ('id', 'nips', 'dates', 'amount',):
        found = list(set(re.get_match(read_by_tesseract, exp)))  # unique
        if exp == 'amount' and found:
            value = max(list(map(float, [element.replace(',', '.')
                                         for element in found])))
            # ^ brutto, netto = brutto/1.23
            found = value
        print(exp, found)
        # print('\n\n', read)


def compare_methods(im):
    for method in ('median', 'mean', 'otsu', 'li'):
        print(3*'=========', '\n', method, '\n')
        print_found(tesseract_read(im, method))
    print("UNPROCESSED", '\n',
          pytesseract.image_to_string(im, lang='pol'))


if __name__ == '__main__':
    # for im in load_images(15):
    #     read = tesseract_read(im, 'otsu', is_plot=False)
    #     print_found(read)

    #     print('\n', 3*'=========', '\n')

    fb = Firebase.getInstance()
    fb.login('tegoproszenieusuwać@test.pl')

    filename = 'test.jpg'
    fb.get_img(filename, 'out/testowy.jpg')