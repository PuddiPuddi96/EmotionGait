import pandas as pd
import sys
import os
from Labeller import Labeller
from preprocessing.Gait import Gait
from preprocessing.GaitAlignment import GaitAlignment
from preprocessing.PoseExtractor import PoseExtractor
from preprocessing.GaitExtractor import GaitExtractor
from Model import Model
from sklearn.metrics import classification_report

def gen_label(data,path_csv):
    labeller = Labeller()
    dataset = labeller.label_extract(path_csv, 'Mode')
    for index, row in dataset.iterrows():
        data['GaitID'].append(row['Gait'])
        data['Etichetta'].append(row['Lable'])

def extract_feature(data,path_csv):

    gaitExtractor = GaitExtractor()
    gaitAlignment = GaitAlignment(30)
    poseExtractor = PoseExtractor()

    for video in os.listdir(path_video):
        if video == '.DS_Store': continue
        p_video = path_video + '/' + video
        gait_name = '{}'.format(video[0:-4])
        gait = Gait(gait_name)
        result = gaitExtractor.extract_gait(p_video)
        gait.setListFrame(result[0])
        poses = poseExtractor.extractPose(gait.getListFrame())
        gait.setPoses(poses)
        poses = gaitAlignment.align(gait.getPoses())
        gait.setPoses(poses)
        for pose, j in zip(gait.getPoses(), range(0, num_frame)):
            data['F0_Fr{}'.format(j)].append(pose.getVolumePose())
            data['F1_Fr{}'.format(j)].append(pose.getDistManoSpallaSX())
            data['F2_Fr{}'.format(j)].append(pose.getDistManoSpallaDX())
            data['F3_Fr{}'.format(j)].append(pose.getDistManoFiancoSX())
            data['F4_Fr{}'.format(j)].append(pose.getDistManoFiancoDX())
            data['F5_Fr{}'.format(j)].append(pose.getDistGomitoFiancoSX())
            data['F6_Fr{}'.format(j)].append(pose.getDistGomitoFiancoDX())
            data['F7_Fr{}'.format(j)].append(pose.getInclinazioneSpalle())
            data['F8_Fr{}'.format(j)].append(pose.getDistCavigliaFiancoSX())
            data['F9_Fr{}'.format(j)].append(pose.getDistCavigliaFiancoDX())
            data['F10_Fr{}'.format(j)].append(pose.getDistCaviglie())



if __name__ == "__main__":

    if len(sys.argv)==3:
        path_video=sys.argv[1]
        path_csv=sys.argv[2]

        data = {'GaitID': [],
                'Etichetta': []
                }
        num_frame = 30
        num_features = 11
        for j in range(0, num_frame):
            for i in range(0, num_features):
                data['F{}_Fr{}'.format(i, j)] = []

        print("Genero le lable")
        gen_label(data,path_csv)

        # Estraggo le features
        print("Estraggo le features")
        extract_feature(data,path_csv)

        print("Eseguo la predizione")
        df = pd.DataFrame(data=data)
        model=Model()
        y_pred=model.predict(df)


    if len(sys.argv)==2:
        path_video = sys.argv[1]

        data = {'GaitID': []
                }
        num_frame = 30
        num_features = 11
        for j in range(0, num_frame):
            for i in range(0, num_features):
                data['F{}_Fr{}'.format(i, j)] = []

        # Estraggo le features
        extract_feature(data,path_csv)

        df = pd.DataFrame(data=data)
        model = Model()
        y_pred = model.predict(df)
        print(y_pred)

