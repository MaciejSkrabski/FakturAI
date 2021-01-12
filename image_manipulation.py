# %%

# %%
# import cv2
import os
import numpy as np
from PIL import Image
from skimage import filters
from matplotlib import pyplot as plt

images = np.asarray([os.path.join('data', file)
                     for file in os.listdir('data')
                     if file[-4:] in ('.png', '.jpg', '.bmp')])


def load_images(size):
    chosen = np.random.choice(images, size=size, replace=False).tolist()
    print(chosen)
    fig = plt.figure(figsize=(8, 6))
    columns = 4
    rows = 2
    data = []
    for i in range(1, columns*rows + 1):
        # img = np.random.randint(8, size=(h, w))
        fig.add_subplot(rows, columns, i)
        im = Image.open(chosen[i-1])
        data.append(im)
        plt.imshow(im)
        plt.axis('off')
    plt.show()
    return data  # return last image


def to_greyscale(image_array):
    # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return np.dot(image_array[..., :3], [0.2989, 0.5870, 0.1140])

# ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)


def binarize(image_array, value):
    binarized = np.zeros_like(image_array, dtype=np.bool_)
    binarized[np.where(image_array <= value)] = 1
    return binarized


def simple_thresh(image_array, method='mean'):
    methods = {'mean': np.mean,
               'median': np.median,
               'li': filters.threshold_li,
               'otsu': filters.threshold_otsu,
               }
    if method not in methods:
        raise Exception('Declared method not in methods')
    return methods[method](image_array)


def plt_gray(image):
    plt.axis("off")
    return plt.imshow(image, cmap='gray')


if __name__ == '__main__':
    image = to_greyscale(np.asarray(load_images(15)[-1], dtype='float32')/255)
    plt_gray(image)
    plt.show()

    otsu = simple_thresh(image, 'otsu')
    li = simple_thresh(image, 'li')
    mean = simple_thresh(image, 'mean')
    median = simple_thresh(image, 'median')
    print(otsu, li, mean, median)

    for i in (otsu, li, mean, median):
        binarized = binarize(image, i)
        plt_gray(binarized)
        plt.show()

# %%
