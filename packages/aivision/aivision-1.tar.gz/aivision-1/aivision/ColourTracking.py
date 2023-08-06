import cv2
import numpy as np


class ColourDetector:
    def __init__(self, lower_colour_value, upper_colour_value):
        self.lower_colour_value = lower_colour_value
        self.upper_colour_value = upper_colour_value

    def mask_colour(self,img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img,self.lower_colour_value,self.upper_colour_value)
        mask = cv2.medianBlur(mask, 3)
        mask_inv = 255 - mask
        mask = cv2.dilate(mask, np.zeros((1,1),np.uint8), 5)
        return mask

    def draw_rect(self,img,mask,areaLimit):
        con1, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for c in con1:
            area = cv2.contourArea(c)
            if area > areaLimit:

                x, y, w, h = cv2.boundingRect(c)
                a = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img


cap = cv2.VideoCapture(0)
up = np.array([0, 50, 50])
low = np.array([10, 255, 255])
cd = ColourDetector(up,low)

while True:
    _,frame = cap.read()
    masker = cd.mask_colour(frame)
    mask = cd.draw_rect(frame,masker,1000)
    cv2.imshow("Mask",mask)
    cv2.waitKey(1)



