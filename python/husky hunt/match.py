import cv2
import numpy as np

img_rgb = cv2.imread('img.png')
img_blank = np.zeros(img_rgb.shape)

def uninvert(letter: str):
    letter = letter.lower()
    start = ord('a')
    end = ord('z')
    current = ord(letter[0])
    delta = current - start
    ret = chr(end - delta)
    # print("Inverse of {} is {}".format(letter, ret))
    return str(ret)

def match(name):

    template = cv2.imread('chars/{}.png'.format(name))
    w, h = template.shape[:-1]

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .9

    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):  # Switch columns and rows
        # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        uninverted = uninvert(name)
        cv2.putText(img_rgb, uninverted, (pt[0], pt[1]+h), cv2.FONT_ITALIC, 1, (0,0,255), 2)
        cv2.putText(img_blank, uninverted, pt, cv2.FONT_ITALIC, 1, (0,0,255), 2)



# import os
# files = os.listdir("chars")

# for path in files:
#     print(path[0])
#     match(path[0])

# cv2.imwrite('result.png', img_rgb)
# cv2.imwrite('blank.png', img_blank)