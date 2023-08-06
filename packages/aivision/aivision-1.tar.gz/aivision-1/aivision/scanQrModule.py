import cv2  # importing the required modules
import numpy as np
from pyzbar.pyzbar import decode


# creating a class so that we can find the contour and use the data

class Scan:
    def __init__(self, img):
        self.img = img
        self.code = decode(self.img)

    # decoding the data of the QR Code
    def decodeData(self):
        return self.code

    # Drawing the landmarks on the QR Code to help recognizing the data
    def drawLandmarks(self,
                      colour=(0, 0, 255),
                      connections=True):
        point = self.code[0][3]

        if connections:
            cv2.line(self.img, point[0], point[1], (0, 255, 0), 2)
            cv2.line(self.img, point[1], point[2], (0, 255, 0), 2)
            cv2.line(self.img, point[2], point[3], (0, 255, 0), 2)
            cv2.line(self.img, point[3], point[0], (0, 255, 0), 2)
        cv2.circle(self.img, point[0], 4, colour, cv2.FILLED)
        cv2.circle(self.img, point[1], 4, colour, cv2.FILLED)
        cv2.circle(self.img, point[2], 4, colour, cv2.FILLED)
        cv2.circle(self.img, point[3], 4, colour, cv2.FILLED)

    def writeDecodedData(self, colour=(0, 0, 255)):
        point = self.code[0][3]
        # cv2.rectangle(self.img, (point[0].x, point[0].y-35), point[3], colour, cv2.FILLED)
        cv2.putText(self.img, str(self.code[0][0]), (int(point[0].x/2), point[0].y), cv2.FONT_HERSHEY_PLAIN, 3, colour, 2)

    def drawRectangle(self,
                      colour=(0,0,225),
                      linetype=None,
                      thickness=None
                      ):
        point = self.code[0][3]
        cv2.rectangle(self.img, point[0], point[3], colour, thickness=thickness)

    



