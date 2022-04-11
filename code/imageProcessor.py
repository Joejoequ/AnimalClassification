import os
import random

import cv2
import numpy as np


def gasuss_noise(image, mean=0, var=0.001):
    image = np.array(image / 255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out * 255)

    return out

def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def compress():
    animalList = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'spider', 'squirrel', 'sheep', 'horse']

    for animal in animalList:
        if not os.path.exists(animal): os.makedirs(animal)
        for i in range(1, 151):

            img = cv2.imread("./raw/" + animal + "/" + str(i) + ".jpg", 1)
            cv2.imwrite("./" + animal + "/" + str(i) + ".jpg", img, [cv2.IMWRITE_JPEG_QUALITY,20])
        print(animal, "Finished")


def addnoise():
    animalList = ['butterfly', 'cat', 'chicken', 'cow', 'dog', 'elephant', 'spider', 'squirrel', 'sheep', 'horse']
    for animal in animalList:
        for i in range(1, 75):
            img = cv2.imread("./raw/" + animal + "/" + str(i) + ".jpg", 1)
            img=sp_noise(img,0.05)
            cv2.imwrite("./" + animal + "/" + str(i+150) + ".jpg", img,[cv2.IMWRITE_JPEG_QUALITY, 20])

        print(animal, "Finished")
    return





if __name__ == '__main__':
    compress()
    addnoise()


