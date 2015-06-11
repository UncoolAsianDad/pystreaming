import cv2
import urllib
import numpy as np
import threading
import pycurl

directions = {
    ord('a'): 5,
    ord('s'): 7,
    ord('d'): 3,
    ord('w'): 1,
    ord('e'): 4
}


class streamingThread(threading.Thread):
    def __init__(self, ip):

        threading.Thread.__init__(self)
        self.winName = "IPCamera" + ip

        self.ip = ip
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        self.c.setopt(pycurl.USERPWD, "%s:%s" % ("admin", "brian123"))
        self.mode = 1
        self.exit = False
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def checkInput(self):
        params = {'PanSingleMoveDegree': '5',
                  'TiltSingleMoveDegree': '5'}

        key = cv2.waitKey(50) & 0xff
        if key == ord('q'):
            self.exit = True
        elif key in directions:
            newParams = params.copy()
            newParams.update({'PanTiltSingleMove': directions[key]})
            self.c.setopt(pycurl.URL, 'http://' + self.ip + '/pantiltcontrol.cgi' + '?' + urllib.urlencode(newParams))
            self.c.perform()
        elif key == ord('z'):
            self.mode = (self.mode + 1) % 3
        elif key in xrange(ord('1'), ord('9'), 1):
            newParams = {'PanTiltPresetPositionMove': key - ord('0')}
            self.c.setopt(pycurl.URL, 'http://' + self.ip + '/pantiltcontrol.cgi' + '?' + urllib.urlencode(newParams))
            self.c.perform()

        return False

    def run(self):

        cv2.namedWindow(self.winName, cv2.CV_WINDOW_AUTOSIZE)
        self.stream = urllib.urlopen('http://' + self.ip + '/video/mjpg.cgi')
        bytes = ''
        while not self.exit:
            bytes += self.stream.read(10240)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')

            ''' decoding the jpg '''
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]

                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = self.clahe.apply(gray)
                ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

                canny = cv2.Canny(thresh, 100, 200)
                if self.mode == 0:
                    cv2.imshow(self.winName, frame)
                elif self.mode == 1:
                    cv2.imshow(self.winName, gray)
                elif self.mode == 2:
                    cv2.imshow(self.winName, canny)

                self.checkInput()

        cv2.destroyWindow('video')


def main():
    thread_lock = threading.Lock()
    thread1 = streamingThread('192.168.1.40')
    thread1.start()
    # thread2 = streamingThread('192.168.1.41')
    # thread2.start()

    print "Exiting Main Thread"


if __name__ == '__main__':
    main()
