# %%
import cv2
import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

images = np.asarray([os.path.join('data', file)
                     for file in os.listdir('data')
                     if file[-4:] == '.png'])


def load_images(size):
    chosen = np.random.choice(images, size=size, replace=False).tolist()
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
    return np.dot(image_array[..., :3], [0.299, 0.587, 0.114])

# ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)


def simple_thresh(image_array, values):
    return cv2.threshold(image_array, *values, cv2.THRESH_BINARY_INV)

# %%
if __name__ == '__main__':
    cmap = plt.get_cmap("gray")
    image = to_greyscale(np.asarray(load_images(15)[-1], dtype='float32'))
    print(image)
    plt.imshow(image, cmap=cmap)
    plt.show()

    ret, thresh1 = simple_thresh(image, (206, 255))
    print(ret)
    plt.imshow(thresh1, cmap=cmap)
    plt.show()
