import copy
import random
import numpy as np
from .Pose import Pose

class GaitAlignment:

    def __init__(self,size):
        self.batchSize=size

    def setBatchSize(self,size): self.batchSize=size
    def getBatchSize(self): return self.batchSize

    def align(self,gait):

        if len(gait) == self.batchSize:
            return gait

        batch = copy.copy(gait)
        if len(gait) < self.batchSize:
            # Eseguo un agumentation dei frame utilizzando la media
            n_frame_mancanti =self.batchSize - len(gait)
            for i in range(n_frame_mancanti):
                pos = random.randint(1, len(gait) - 2)
                batch.insert(pos, self.generate_sintetic_pose(batch[pos - 1], batch[pos + 1]))
            return batch
        else:
            # Eseguo una riduzione dei frame
            n_frame_superiori = len(gait) - self.batchSize
            for i in range(n_frame_superiori):
                pos = random.randint(2, len(batch) - 1 - i)
                batch.pop(pos)
            return batch

    def generate_sintetic_pose(self,pose1, pose2):
        pose=Pose()
        sintetic_landmark = []
        for landmark1, landmark2 in zip(pose1.getLandmark(), pose2.getLandmark()):
            x = np.mean((landmark1[0] + landmark2[0]) / 2)
            y = np.mean((landmark1[1] + landmark2[1]) / 2)
            sintetic_landmark.append((x, y))
        pose.setLandmark(sintetic_landmark)
        return pose
