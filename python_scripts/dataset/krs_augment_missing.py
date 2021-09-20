import numpy as np
import pandas as pd
import datetime
import pickle
from tqdm import tqdm
import sys
sys.path.append('../models')
from krs_model import XGBoostModel

class KRS:
    def __init__(self, max_storage, inflow_df):
        self.max_storage = max_storage

        self.weather_df = pd.read_csv('Weather/mysuru_kodagu_hassan_weather.csv')
        self.inflow_df = inflow_df
        self.season_df = self.inflow_df[['MONTH', 'DATE', 'SEASON']].drop_duplicates()
        self.normal_inflow_outflow_df = pd.read_csv('datewise_normal_inflow_outflow.csv')

        # Load encoders
        with open('../training/KRS/encoders/month_le.pkl', 'rb') as f:
            self.month_le = pickle.load(f)
        with open('../training/KRS/encoders/date_le.pkl', 'rb') as f:
            self.date_le = pickle.load(f)
        with open('../training/KRS/encoders/season_le.pkl', 'rb') as f:
            self.season_le = pickle.load(f)
        
        with open('../training/KRS/encoders/rs_inflow.pkl', 'rb') as f:
            self.rs_inflow = pickle.load(f)
        with open('../training/KRS/encoders/rs_outflow.pkl', 'rb') as f:
            self.rs_outflow = pickle.load(f)
        with open('../training/KRS/encoders/rs_temp.pkl', 'rb') as f:
            self.rs_temp = pickle.load(f)
        with open('../training/KRS/encoders/rs_feels_like.pkl', 'rb') as f:
            self.rs_feels_like = pickle.load(f)
        with open('../training/KRS/encoders/rs_temp_min.pkl', 'rb') as f:
            self.rs_temp_min = pickle.load(f)
        with open('../training/KRS/encoders/rs_temp_max.pkl', 'rb') as f:
            self.rs_temp_max = pickle.load(f)
        with open('../training/KRS/encoders/rs_pressure.pkl', 'rb') as f:
            self.rs_pressure = pickle.load(f)
        with open('../training/KRS/encoders/rs_humidity.pkl', 'rb') as f:
            self.rs_humidity = pickle.load(f)
        with open('../training/KRS/encoders/rs_wind_speed.pkl', 'rb') as f:
            self.rs_wind_speed = pickle.load(f)
        with open('../training/KRS/encoders/rs_wind_deg.pkl', 'rb') as f:
            self.rs_wind_deg = pickle.load(f)
        with open('../training/KRS/encoders/rs_rain.pkl', 'rb') as f:
            self.rs_rain = pickle.load(f)
        with open('../training/KRS/encoders/rs_clouds_all.pkl', 'rb') as f:
            self.rs_clouds_all = pickle.load(f)

        # weather data district df
        self.kodagu_df = self.weather_df[self.weather_df['city_name'] == 'Kodagu'].reset_index(drop=True)
        self.hassan_df = self.weather_df[self.weather_df['city_name'] == 'Hassan'].reset_index(drop=True)
        self.mysuru_df = self.weather_df[self.weather_df['city_name'] == 'Mysuru'].reset_index(drop=True)

        # region-wise weather data scaling
        self.__apply_scaling(self.kodagu_df)
        self.__apply_scaling(self.hassan_df)
        self.__apply_scaling(self.mysuru_df)

        self.__load_models()

    def __apply_scaling(self, df):
        df['temp'] = self.rs_temp.transform(df[['temp']]).flatten()
        df['feels_like'] = self.rs_feels_like.transform(df[['feels_like']]).flatten()
        df['temp_min'] = self.rs_temp_min.transform(df[['temp_min']]).flatten()
        df['temp_max'] = self.rs_temp_max.transform(df[['temp_max']]).flatten()
        df['pressure'] = self.rs_pressure.transform(df[['pressure']]).flatten()
        df['humidity'] = self.rs_humidity.transform(df[['humidity']]).flatten()
        df['wind_speed'] = self.rs_wind_speed.transform(df[['wind_speed']]).flatten()
        df['wind_deg'] = self.rs_wind_deg.transform(df[['wind_deg']]).flatten()
        df['rain'] = self.rs_rain.transform(df[['rain']]).flatten()
        df['clouds_all'] = self.rs_clouds_all.transform(df[['clouds_all']]).flatten()
        df.loc[:, ('broken clouds', 'overcast clouds', 'scattered clouds', 'sky is clear',
            'few clouds', 'fog', 'light rain', 'mist', 'haze', 'moderate rain',
            'heavy intensity rain', 'light intensity drizzle', 'drizzle',
            'heavy intensity drizzle', 'very heavy rain',
            'thunderstorm with heavy rain', 'thunderstorm with rain',
            'thunderstorm', 'proximity shower rain', 'thunderstorm with light rain',
            'shower rain', 'light intensity shower rain', 'light thunderstorm')] = df.loc[:, ('broken clouds', 'overcast clouds', 'scattered clouds', 'sky is clear',
            'few clouds', 'fog', 'light rain', 'mist', 'haze', 'moderate rain',
            'heavy intensity rain', 'light intensity drizzle', 'drizzle',
            'heavy intensity drizzle', 'very heavy rain',
            'thunderstorm with heavy rain', 'thunderstorm with rain',
            'thunderstorm', 'proximity shower rain', 'thunderstorm with light rain',
            'shower rain', 'light intensity shower rain', 'light thunderstorm')] / 24

    def __load_models(self):
        self.inflow_model = XGBoostModel('../models/krs_inflow_xgboost.json')
        self.outflow_model = XGBoostModel('../models/krs_outflow_xgboost.json')

    def __predict(self, loop_date):
        month = loop_date.month
        date = loop_date.day
        season = self.season_df[(self.season_df['DATE'] == date) & (self.season_df['MONTH'] == month)]['SEASON'].values[0]

        prev_date_list = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, 1)]
        sel_kodagu = self.kodagu_df[self.kodagu_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()
        sel_hassan = self.hassan_df[self.hassan_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()
        sel_mysuru = self.mysuru_df[self.mysuru_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()

        prev_inflow_dates = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, 0)]
        sel_inflow = self.inflow_df[(self.inflow_df['FLOW_DATE'].isin(prev_inflow_dates)) & (self.inflow_df['RESERVOIR'] == 'K.R.S')]['INFLOW_CUSECS'].values.flatten()

        month_transformed = self.month_le.transform([month])
        date_transformed = self.date_le.transform([date])
        season_transformed = self.season_le.transform([season])
        inflow_prediction_input = np.concatenate([month_transformed, date_transformed, season_transformed, sel_mysuru, sel_kodagu, sel_hassan, self.rs_inflow.transform([sel_inflow])[0]]).reshape(1, -1)

        y_hat_inflow = self.inflow_model(inflow_prediction_input)
        y_hat_inflow = self.rs_inflow.inverse_transform([[y_hat_inflow.item()]])[0][0]
        y_hat_inflow = round(y_hat_inflow) if y_hat_inflow > 0 else 0

        outflow_prediction_input = np.concatenate([month_transformed, date_transformed, season_transformed, sel_mysuru, self.rs_inflow.transform([sel_inflow])[0], self.rs_inflow.transform([[y_hat_inflow]])[0]]).reshape(1, -1)
        y_hat_outflow = self.outflow_model(outflow_prediction_input)
        y_hat_outflow = self.rs_outflow.inverse_transform([[y_hat_outflow.item()]])[0][0]
        y_hat_outflow = round(y_hat_outflow)
        y_hat_outflow = y_hat_outflow if y_hat_outflow > 0 else 0
        
        return round(y_hat_inflow), round(y_hat_outflow)
    
    def __get_storage(self, actual_inflow, outflow, curr_storage):
        actual_inflow_tmc = 8.64e-05 * actual_inflow
        pred_outflow_tmc = 8.64e-05 * outflow
        storage = curr_storage + actual_inflow_tmc
        if pred_outflow_tmc > storage or storage == 0:
            outflow = 11574.074 * storage
            storage = 0
        else:
            storage -= pred_outflow_tmc
        
        if storage > self.max_storage:
            outflow += 11574.074 * (storage - self.max_storage)
            storage = self.max_storage
        
        return storage, round(outflow)

    def get_prediction(self, loop_date, prev_storage):
        #predict
        inflow, outflow = self.__predict(loop_date)
        
        # for debugging
        if np.isnan(outflow):
            print(loop_date)

        if prev_storage is not None:
            storage, outflow = self.__get_storage(inflow, outflow, prev_storage)
        return inflow, outflow


inflow_df = pd.read_csv('reservoir_dataset.csv')
krs_obj = KRS(max_storage=49.45, inflow_df=inflow_df)
loop_date = datetime.date(2011, 6, 1)
end_date = datetime.date(2021, 6, 1)
delta = datetime.timedelta(days=1)
pbar = tqdm(total=(end_date-loop_date).days, initial=1)
while loop_date < end_date:
    index = inflow_df[(inflow_df['FLOW_DATE'] == str(loop_date)) & (inflow_df['RESERVOIR'] == 'K.R.S')].index
    if len(index) == 0:
        index = inflow_df.shape[0]
        prev_storage = inflow_df[(inflow_df['FLOW_DATE'] == str(loop_date - datetime.timedelta(days=1))) & (inflow_df['RESERVOIR'] == 'K.R.S')]['PRESENT_STORAGE_TMC'].values
        prev_storage = prev_storage[0] if len(prev_storage) > 0 else None
        pred_inflow, pred_outflow = krs_obj.get_prediction(loop_date, prev_storage)
        inflow_df.loc[index, 'FLOW_DATE'] = str(loop_date)
        inflow_df.loc[index, 'RESERVOIR'] = 'K.R.S'
        inflow_df.loc[index, 'INFLOW_CUSECS'] = pred_inflow
        inflow_df.loc[index, 'OUTFLOW_CUECS'] = pred_outflow
        inflow_df.loc[index, 'YEAR'] = loop_date.year
        inflow_df.loc[index, 'MONTH'] = loop_date.month
        inflow_df.loc[index, 'DATE'] = loop_date.day
    
    loop_date += delta
    pbar.update(1)
inflow_df.to_csv('reservoir_dataset_augmented.csv', index=False)