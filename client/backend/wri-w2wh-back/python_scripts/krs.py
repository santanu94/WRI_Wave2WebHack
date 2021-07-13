import pandas as pd
import torch
from models import inflow_models as im
from models.outflow_model import OutflowModel
import pickle
import json

class KRS:
    def __init__(self):
        self.rainfall_departure_df = pd.read_csv('dataset/Rainfall 2010-2020/rainfall_departure_dataset.csv')
        self.rainfall_departure_df = self.rainfall_departure_df[self.rainfall_departure_df['DISTRICTS'] == 'KODAGU']
        self.rainfall_departure_df.drop(columns=['DISTRICTS'], inplace=True)

        with open('dataset/month_le.pkl', 'rb') as f:
            self.month_le = pickle.load(f)

        with open('dataset/date_le.pkl', 'rb') as f:
            self.date_le = pickle.load(f)

        with open('dataset/season_le.pkl', 'rb') as f:
            self.season_le = pickle.load(f)

        self.month_date_day_season_df = pd.read_csv('dataset/month_date_day_season.csv')
        self.month_date_day_season_df.sort_values(by=['MONTH', 'DATE'])

        self.device = self.__get_device()
        self.__load_models()
        

    def __get_device(self):
        if torch.cuda.is_available():
            return torch.device('cuda')
        else:
            return torch.device('cpu')
    
    def __load_models(self):
        nmonths = len(self.month_le.classes_)
        ndate = len(self.date_le.classes_)
        nseasons = len(self.season_le.classes_)
        
        self.inflow_model = im.KRSInflowModel(nmonths, ndate, nseasons).to(self.device)
        self.inflow_model.load_state_dict(torch.load('models/inflow_cnn_date.pth', map_location=self.device))
        self.inflow_model.eval()
        
        self.outflow_model = OutflowModel(nmonths, ndate, nseasons).to(self.device)
        self.outflow_model.load_state_dict(torch.load('models/krs_outflow_bestmodel.pth', map_location=self.device))
        self.outflow_model.eval()

    def __predict(self, month, date, season, year, prev_storage):
        prev_rainfall_departure_df = self.rainfall_departure_df[(self.rainfall_departure_df['YEAR'] < year) & (self.rainfall_departure_df['MONTH'] == month)].sort_values('YEAR', ascending=False).head(3)
        prev_avg_rainfall = prev_rainfall_departure_df['RAINFALL'].values.mean()
        prev_avg_departure = prev_rainfall_departure_df['DEPARTURE'].values.mean()
        prev_avg_outflow = self.prev_predictions[self.prev_predictions['DD-MM-YYYY'].str.startswith(f'{date}-{month}')]['OUTFLOW'].mean()

        month_transformed = self.month_le.transform([month])
        date_transformed = self.date_le.transform([date])
        season_transformed = self.season_le.transform([season])

        x_month = torch.tensor(month_transformed).to(self.device)
        x_date = torch.tensor(date_transformed).to(self.device)
        x_season = torch.tensor(season_transformed).to(self.device)
        x_prev_rain_data = torch.FloatTensor([prev_avg_rainfall, prev_avg_departure]).view(1, -1).to(self.device)

        with torch.no_grad():
            y_hat_inflow = self.inflow_model(x_month, x_date, x_season, x_prev_rain_data)
            x_inflow_prev_avg_outflow = torch.FloatTensor([y_hat_inflow, prev_avg_outflow]).view(1, -1).to(self.device)
            y_hat_outflow = self.outflow_model(x_month, x_date, x_season, x_inflow_prev_avg_outflow)

        y_hat_inflow = y_hat_inflow.view(1).cpu().item()
        y_hat_outflow = y_hat_outflow.view(1).cpu().item()
        
        pred_inflow_tmc = 8.64e-05 * y_hat_inflow
        pred_outflow_tmc = 8.64e-05 * y_hat_outflow
        storage = prev_storage + pred_inflow_tmc
        if pred_outflow_tmc > storage:
            y_hat_outflow = 11574.074 * storage
            storage = 0
        else:
            storage -= pred_outflow_tmc
        
        return y_hat_inflow, y_hat_outflow, storage

    def get_predictions(self, prev_storage, year):
        prediction = {}
        prediction['INFLOW'] = {}
        prediction['OUTFLOW'] = {}
        prediction['STORAGE'] = {}

        self.prev_predictions = None
        for i in range(1, 4):
            if year-i >= 2011:
                with open(f'predictions/KRS_inflow_{year-i}.json') as f:
                    if self.prev_predictions is None:
                        self.prev_predictions = pd.DataFrame(json.load(f)).reset_index()
                        self.prev_predictions.rename(columns={'index': 'DD-MM-YYYY'}, inplace=True)
                    else:
                        data_df = pd.DataFrame(json.load(f)).reset_index()
                        data_df.rename(columns={'index': 'DD-MM-YYYY'}, inplace=True)
                        self.prev_predictions = self.prev_predictions.append(data_df, ignore_index=True)

        if self.prev_predictions is None:
            outflow_df = pd.read_csv('dataset/reservoir_dataset.csv')
            outflow_df = outflow_df[(outflow_df['RESERVOIR'] == 'K.R.S') & (outflow_df['YEAR'] == 2011)]
            outflow_df['DD-MM-YYYY'] = outflow_df['DATE'].astype(str) + '-' + outflow_df['MONTH'].astype(str) + '-' + outflow_df['YEAR'].astype(str)
            self.prev_predictions = outflow_df
            self.prev_predictions.rename(columns={'OUTFLOW_CUECS': 'OUTFLOW'}, inplace=True)

        for idx, row in self.month_date_day_season_df.iterrows():
            month = row['MONTH']
            date = row['DATE']
            day = row['DAY']
            season = row['SEASON']

            if year % 4 != 0 and month == 2 and date == 29:
                continue
            inflow, outflow, storage = self.__predict(month, date, season, year, prev_storage)

            prediction['INFLOW'][f'{date}-{month}-{year}'] = inflow
            prediction['OUTFLOW'][f'{date}-{month}-{year}'] = outflow
            prediction['STORAGE'][f'{date}-{month}-{year}'] = storage

        return prediction
