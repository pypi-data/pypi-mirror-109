import cv2
import numpy


class Chroma:
    def __init__(self,lower_colour_value,upper_colour_value):
        self.lower_colour_value = lower_colour_value
        self.upper_colour_value = upper_colour_value

    def add_chroma(self,frame,bgImg,kernel= numpy.ones((7, 7), numpy.uint8)):

        inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(inspect, self.lower_colour_value, self.upper_colour_value)
        mask = cv2.medianBlur(mask, 3)
        mask_inv = 255 - mask
        mask = cv2.dilate(mask, kernel, 5)

        # The mixing of frames in a combination to achieve the required frame
        b = frame[:, :, 0]
        g = frame[:, :, 1]
        r = frame[:, :, 2]
        b = cv2.bitwise_and(mask_inv, b)
        g = cv2.bitwise_and(mask_inv, g)
        r = cv2.bitwise_and(mask_inv, r)
        frame_inv = cv2.merge((b, g, r))
        Frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        blanket = cv2.cvtColor(bgImg, cv2.COLOR_RGB2BGR)
        b = bgImg[:, :, 0]
        g = bgImg[:, :, 1]
        r = bgImg[:, :, 2]
        b = cv2.bitwise_and(mask, b)
        g = cv2.bitwise_and(mask, g)
        r = cv2.bitwise_and(mask, r)
        blanket_area = cv2.merge((b, g, r))
        final = cv2.bitwise_or(blanket_area, frame_inv)
        return final

