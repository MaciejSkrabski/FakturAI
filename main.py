# %%
import numpy as np
import pytesseract
import argparse
import cv2
from matplotlib import pyplot as plt

from image_manipulation import (
    load_images,
    to_greyscale,
    simple_thresh)
# %%
for im in load_images(30):
    print(im)
    grey = to_greyscale(np.asarray(im, dtype='float32'))
    thresh = simple_thresh(grey, (206, 255))[1]

    # kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1000))

    # max value in kernel's region
    dilation = cv2.convertScaleAbs(cv2.dilate(thresh, kernel, iterations=1))
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)
    copied = np.array(im, copy=True)
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)

        # highlight region
        draw = cv2.rectangle(copied, (x, y),
                             (x + w, y + h),
                             (180, 0, 0), 1)
        # modyfying block before ocr
        mod = copied[y: y + h, x: x + w]
        text = pytesseract.image_to_string(mod, lang='pol')
        print(text)


