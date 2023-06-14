import copy
import cv2
import numpy as np
from matplotlib import pyplot as plt
import mediapipe as mp


class Gait:

    def __init__(self,gaitId):
        self.gaitId=gaitId
        self.poses=None
        self.frames=None

    def getListFrame(self): return self.frames

    def setListFrame(self,listFrame): self.frames=listFrame
    def getPoses(self): return self.poses
    def setPoses(self,poses): self.poses=poses

    def getGaitId(self):return self.gaitId
    def setGaitId(self,id): self.gaitId=id

    def printGait(self):
        for pose in self.poses:
            pose.printPose()



