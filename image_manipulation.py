# %%

# %%
import numpy as np
from PIL import Image
from skimage import filters
from matplotlib import pyplot as plt


def open_image(im_path):
    try:
        im = Image.open(im_path)
        data = np.asarray(im)
        return data

    except Exception as e:
        print('Nie można otworzyć pliku. Upewnij się, że plik istnieje',
              'oraz że podana ścieżka jest prawidłowa.\n', e)


def to_greyscale(image_array):
    return np.dot(image_array[..., :3], [0.2989, 0.5870, 0.1140])


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
    image = open_image('out/testow.jpg')
    image = to_greyscale(image)
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
