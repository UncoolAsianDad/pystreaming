import cv2
import urllib
import numpy as np


def playvideo(url):
    stream = urllib.urlopen(url)
    bytes = ''
    while True:
        bytes += stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            # gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(i, 127, 255, cv2.THRESH_BINARY)
            canny = cv2.Canny(thresh, 100, 200)
            cv2.imshow('i', canny)
            if cv2.waitKey(1) == 27:
                return


playvideo('http://camera1/video/mjpg.cgi')
