import copy
import cv2
import numpy as np



class GaitExtractor:

    def extract_gait(self,video):
        loops = []
        list_frame = []
        first_frame = None
        pre_diff = 0
        threshold = 2

        vid = cv2.VideoCapture(video)

        while (True):
            ret, frame = vid.read()
            if ret:
                if first_frame is None:
                    first_frame = frame
                    list_frame.append(frame)
                else:
                    diff, _ = self.mse(frame, first_frame)
                    if diff < pre_diff and pre_diff - diff > threshold:
                        loops.append(copy.copy(list_frame))

                        list_frame.clear()
                        list_frame.append(frame)
                        first_frame = frame
                        pre_diff = 0
                    else:
                        pre_diff = diff
                        list_frame.append(frame)

            else:
                break

        return loops


    def mse(self,img1, img2):
        img1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        return mse, diff