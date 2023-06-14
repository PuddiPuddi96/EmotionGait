import mediapipe as mp
import cv2
import math
from .Pose import Pose
class PoseExtractor:

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose

    def extractPose(self,gait):
        list_pose=[]
        with self.mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True,
                            min_detection_confidence=0.4) as pose:
            for frame in gait:
                results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                list_pose.append(results.pose_landmarks.landmark)
        #Clipping Det
        pose_clippate = self.clipping_detection(list_pose)
        pose_clippate.sort()

        pose_pulite = []
        for id_frame in range(len(list_pose)): #Rimuovo i frame clippati
            if id_frame in pose_clippate:
                continue
            pose_pulite.append(list_pose[id_frame])

        #Convert le pose pulite in Pose
        list_pose=[]
        for pose in pose_pulite:
            p=Pose()
            p.convertMediaPipePose(pose)
            list_pose.append(p)
        return list_pose

    def clipping_detection(self,list_pose):

        frame_clippati = []
        # Larghezza spalle primo frame
        pose = list_pose[0]
        dist = math.sqrt(math.pow(pose[11].x - pose[12].x, 2) +
                            math.pow(pose[11].y - pose[12].y, 2))

        for pose, i in zip(list_pose[1:], range(len(list_pose[1:]))):
            dist_spalle = math.sqrt(math.pow(pose[11].x - pose[12].x, 2) +
                                    math.pow(pose[11].y - pose[12].y, 2))
            if dist_spalle < dist * 80 / 100:
                frame_clippati.append(i + 1)

        # Larghezza bacino primo frame
        pose = list_pose[0]
        dist = math.sqrt(math.pow(pose[23].x - pose[24].x, 2) +
                            math.pow(pose[23].y - pose[24].y, 2))

        for pose, i in zip(list_pose[1:], range(len(list_pose[1:]))):
            dist_spalle = math.sqrt(math.pow(pose[23].x - pose[24].x, 2) +
                                    math.pow(pose[23].y - pose[24].y, 2))
            if dist_spalle < dist * 80 / 100:
                if not i + 1 in frame_clippati:
                    frame_clippati.append(i + 1)

        # Distanza gomiti primo frame
        pose = list_pose[0]
        dist = math.sqrt(math.pow(pose[13].x - pose[14].x, 2) +
                            math.pow(pose[13].y - pose[14].y, 2))

        for pose, i in zip(list_pose[1:], range(len(list_pose[1:]))):
            dist_gomiti = math.sqrt(math.pow(pose[13].x - pose[14].x, 2) +
                                    math.pow(pose[13].y - pose[14].y, 2))
            if dist_gomiti < dist * 80 / 100:
                if not i + 1 in frame_clippati:
                    frame_clippati.append(i + 1)

        # Distanza polsi primo frame
        pose = list_pose[0]
        dist = math.sqrt(math.pow(pose[15].x - pose[16].x, 2) +
                            math.pow(pose[15].y - pose[16].y, 2))

        for pose, i in zip(list_pose[1:], range(len(list_pose[1:]))):
            dist_polsi = math.sqrt(math.pow(pose[15].x - pose[16].x, 2) +
                                    math.pow(pose[15].y - pose[16].y, 2))
            if dist_polsi < dist * 80 / 100:
                if not i + 1 in frame_clippati:
                    frame_clippati.append(i + 1)

        # Verifico se le braccia si incrociano
        for pose, i in zip(list_pose[0:], range(len(list_pose[0:]))):

            if (pose[12].x < pose[11].x and pose[13].x < pose[14].x) or (
                    pose[12].x > pose[11].x and pose[13].x > pose[14].x):
                if not i in frame_clippati:
                    frame_clippati.append(i)

            if (pose[14].x < pose[13].x and pose[15].x < pose[16].x) or (
                    pose[14].x > pose[13].x and pose[15].x > pose[16].x):
                if not i in frame_clippati:
                    frame_clippati.append(i)

        return frame_clippati