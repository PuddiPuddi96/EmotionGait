import math
import mediapipe as mp
from matplotlib import pyplot as plt


class Pose:

    def __init__(self):
        self.lendmarkList=None

    def convertMediaPipePose(self, mpPose):
        self.lendmarkList=[]
        for landmark in mpPose:
            self.lendmarkList.append([landmark.x,landmark.y])
        if self.lendmarkList[12][0] > self.lendmarkList[11][0]: #Verifico se la posa è ribaltata
            i=11
            while (i<len(self.lendmarkList)-1):
                j = i + 1
                self.lendmarkList[i], self.lendmarkList[j] = self.lendmarkList[j], self.lendmarkList[i]
                i = j + 1

        return self.lendmarkList

    def getLandmark(self): return self.lendmarkList

    def setLandmark(self,list_landmark): self.lendmarkList=list_landmark
    def getVolumePose(self):

        x1 = self.lendmarkList[11][0]
        x2 = self.lendmarkList[11][0]
        y1 = self.lendmarkList[11][1]
        y2 = self.lendmarkList[11][1]

        i=0
        for landmark in self.lendmarkList[1:]:
            if i in range(0, 10):
                i = i + 1
                continue
            if landmark[0] < x1: x1 = landmark[0]
            if landmark[0] > x2: x2 = landmark[0]
            if landmark[1] < y1: y1 = landmark[1]
            if landmark[1] > y2: y2 = landmark[1]
            i=i+1
        w, h = x2 - x1, y2 - y1
        area = w * h
        return area
    def getDistManoSpallaSX(self):
        return self.distance(self.lendmarkList[15][0], self.lendmarkList[15][1], self.lendmarkList[11][0],
                                self.lendmarkList[11][1])
    def getDistManoSpallaDX(self):
        return self.distance(self.lendmarkList[16][0], self.lendmarkList[16][1], self.lendmarkList[12][0],
                                self.lendmarkList[12][1])
    def getDistManoFiancoSX(self):
        return self.distance(self.lendmarkList[15][0], self.lendmarkList[15][1], self.lendmarkList[23][0],
                                self.lendmarkList[23][1])
    def getDistManoFiancoDX(self):
        return self.distance(self.lendmarkList[16][0], self.lendmarkList[16][1], self.lendmarkList[24][0],
                                self.lendmarkList[24][1])
    def getDistGomitoFiancoSX(self):
        return self.distance(self.lendmarkList[13][0], self.lendmarkList[13][1], self.lendmarkList[23][0],
                                self.lendmarkList[23][1])
    def getDistGomitoFiancoDX(self):
        return self.distance(self.lendmarkList[14][0], self.lendmarkList[14][1], self.lendmarkList[24][0],
                                self.lendmarkList[24][1])
    def getInclinazioneSpalle(self):
        spalla_dx=self.lendmarkList[12]
        spalla_sx=self.lendmarkList[11]
        return (spalla_dx[1] - spalla_sx[1]) / (spalla_dx[0] - spalla_sx[0])
    def getDistCavigliaFiancoSX(self):
        return self.distance(self.lendmarkList[23][0], self.lendmarkList[23][1], self.lendmarkList[27][0],
                        self.lendmarkList[27][1])
    def getDistCavigliaFiancoDX(self):
        return self.distance(self.lendmarkList[24][0], self.lendmarkList[24][1], self.lendmarkList[28][0],
                        self.lendmarkList[28][1])
    def getDistCaviglie(self):
        return self.distance(self.lendmarkList[28][0], self.lendmarkList[28][1], self.lendmarkList[27][0],
                        self.lendmarkList[27][1])

    def printPose(self):
        mp_pose = mp.solutions.pose
        plt.clf()
        landmark_to_skip = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 29, 30, 31, 32]
        for landmark,j in zip(self.lendmarkList,range(len(self.lendmarkList))):
            if j in landmark_to_skip: continue
            plt.scatter(landmark[0], -landmark[1], s=100, c='r')

        for connection in mp_pose.POSE_CONNECTIONS:
            if connection[0] in landmark_to_skip or connection[1] in landmark_to_skip: continue
            plt.plot([self.lendmarkList[connection[0]][0], self.lendmarkList[connection[1]][0]],
                        [-self.lendmarkList[connection[0]][1], -self.lendmarkList[connection[1]][1]],
                        color='k', linewidth='3')
        plt.show()


    def distance(self,x1, y1, x2, y2):
        d = math.sqrt(math.pow(x2 - x1, 2) +
                        math.pow(y2 - y1, 2))
        return d