import cv2
import urllib
import numpy as np
import threading
import pycurl


class streamingThread(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        self.c.setopt(pycurl.USERPWD, "%s:%s" % ("admin", "Cloudno9"))

    def checkInput(self):
        params = {'PanSingleMoveDegree': '5',
                  'TiltSingleMoveDegree': '5'}

        key = cv2.waitKey(50)
        if key & 0xff == ord('a'):
            newParams = params.copy()
            newParams.update({'PanTiltSingleMove': '5'})
            self.c.setopt(pycurl.URL, 'http://' + self.ip + '/pantiltcontrol.cgi' + '?' + urllib.urlencode(newParams))
            self.c.perform()
        elif key & 0xff == ord('s'):
            newParams = params.copy()
            newParams.update({'PanTiltSingleMove': '7'})
            self.c.setopt(pycurl.URL, 'http://' + self.ip + '/pantiltcontrol.cgi' + '?' + urllib.urlencode(newParams))
            self.c.perform()
        elif key & 0xff == ord('d'):
            newParams = params.copy()
            newParams.update({'PanTiltSingleMove': '3'})
            self.c.setopt(pycurl.URL, 'http://' + self.ip + '/pantiltcontrol.cgi' + '?' + urllib.urlencode(newParams))
            self.c.perform()
        elif key & 0xff == ord('w'):
            newParams = params.copy()
            newParams.update({'PanTiltSingleMove': '1'})
            self.c.setopt(pycurl.URL, 'http://' + self.ip + '/pantiltcontrol.cgi' + '?' + urllib.urlencode(newParams))
            self.c.perform()
        elif key & 0xff == ord('e'):
            newParams = params.copy()
            newParams.update({'PanTiltSingleMove': '4'})
            self.c.setopt(pycurl.URL, 'http://' + self.ip + '/pantiltcontrol.cgi' + '?' + urllib.urlencode(newParams))
            self.c.perform()
        elif key & 0xff == 27:
            return True

        return False

    def run(self):
        stream = urllib.urlopen('http://' + self.ip + '/video/mjpg.cgi')
        bytes = ''
        while True:
            bytes += stream.read(10240)
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

                if self.checkInput():
                    break

        cv2.destroyWindow('i')
        print "exiting"
        # time.sleep(1)


def main():
    thread_lock = threading.Lock()
    thread1 = streamingThread('192.168.1.40')
    thread1.start()

    print "Exiting Main Thread"


main()
