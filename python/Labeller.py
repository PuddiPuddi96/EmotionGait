import pandas as pd
import numpy as np

class Labeller:

    def label_extract(self,PATH_DATA,metirc='Mean'):
        dataset=pd.read_excel(PATH_DATA).drop([0])
        if metirc=='Mode':
            df=self.mode_calculator(dataset)
        else:
            df = self.mean_calculator(dataset)

        list_lable = []
        for index, row in df.iterrows():
            if row['Happy'] >= row['Angry'] and row['Happy'] >= row['Sad'] and row['Happy'] >= row['Neutral']:
                list_lable.append(0)
                continue
            if row['Angry'] >= row['Happy'] and row['Angry'] >= row['Sad'] and row['Angry'] >= row['Neutral']:
                list_lable.append(1)
                continue
            if row['Sad'] >= row['Angry'] and row['Sad'] >= row['Happy'] and row['Sad'] >= row['Neutral']:
                list_lable.append(2)
                continue
            if row['Neutral'] >= row['Angry'] and row['Neutral'] >= row['Happy'] and row['Neutral'] >= row['Sad']:
                list_lable.append(3)
                continue
        data = {'Gait': df['Gait'],
                'Lable': list_lable,
                }
        df = pd.DataFrame(data=data)
        return df

    def mean_calculator(self,dataset):
        list_gait = []
        mean_happy = []
        mean_angry = []
        mean_sad = []
        mean_neutral = []

        # Estaggo la media per ogni gati di ogni emozione
        for i in range(1, dataset.shape[1] - 1, 4):
            list_gait.append(dataset.columns[i])
            for j in range(0, 4):
                column_name = dataset.columns[i + j]
                vmean = dataset[column_name].mean()
                if j == 0: mean_happy.append(vmean)
                if j == 1: mean_angry.append(vmean)
                if j == 2: mean_sad.append(vmean)
                if j == 3: mean_neutral.append(vmean)

        data = {'Gait': list_gait,
                'Happy': mean_happy,
                'Angry': mean_angry,
                'Sad': mean_sad,
                'Neutral': mean_neutral
                }

        df = pd.DataFrame(data=data)
        return df


    def mode_calculator(self,dataset):
        list_gait = []
        mode_happy = []
        mode_angry = []
        mode_sad = []
        mode_neutral = []

        # Estaggo la media per ogni gati di ogni emozione
        for i in range(1, dataset.shape[1] - 1, 4):
            list_gait.append(dataset.columns[i])
            for j in range(0, 4):
                column_name = dataset.columns[i + j]
                vmode = dataset[column_name].mode().max()
                if j == 0: mode_happy.append(vmode)
                if j == 1: mode_angry.append(vmode)
                if j == 2: mode_sad.append(vmode)
                if j == 3: mode_neutral.append(vmode)
                
        data = {'Gait': list_gait,
                'Happy': mode_happy,
                'Angry': mode_angry,
                'Sad': mode_sad,
                'Neutral': mode_neutral
                }

        df = pd.DataFrame(data=data)
        return df
