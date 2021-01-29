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
    to_greyscale,
    simple_thresh,
    binarize,
    plt_gray,
    open_image,
    )
from regular_expressions import RegularExpressions
from class_xml import Invoice

mpl.rcParams['figure.dpi'] = 300


def tesseract_read(im_path, method='otsu', lang="pol", is_plot=False):
    im = open_image(im_path)
    grey = to_greyscale(np.asarray(im, dtype='float32'))/255
    thresh = simple_thresh(grey, method)
    binarized = binarize(grey, thresh)
    if is_plot:
        plt_gray(grey)
        plt.show()
        plt_gray(binarized)
        plt.show()

    text = pytesseract.image_to_string(binarized, lang=lang)
    return text


if __name__ == '__main__':
    fb = Firebase.getInstance()
    fb.login('tegoproszenieusuwac@test.pl')

    filename = 'test.jpg'
    output = 'out/testowy.jpg'
    fb.get_img(filename, output)

    text = tesseract_read(output, is_plot=True)

    invoice = Invoice()
    re_obj = RegularExpressions()

    invoice.id = re_obj.get_match(text, 'id')
    invoice.date = re_obj.get_match(text, 'dates')
    invoice.set_nips(re_obj.get_match(text, 'nips'))
    invoice.amount = re_obj.get_match(text, 'amount')

    print(invoice.to_xml_item())


# %%
