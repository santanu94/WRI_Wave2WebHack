import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.shape_base import block
from numpy.lib.function_base import append
import pandas as pd
import torch
from xgboost import data
from models.krs_model import XGBoostModel
import datetime
import pickle
import re

class KRS:
    def __init__(self, max_storage, curr_storage, year):
        self.max_storage = max_storage
        self.curr_amcs_storage = curr_storage
        self.curr_non_amcs_storage = curr_storage
        self.cycle_end_date = datetime.date(year+1, 5, 31)
        self.cum_inflow_till_prev_day = 0
        self.cum_outflow_till_prev_day = 0
        self.normal_cum_inflow_till_prev_day = 0
        # self.remaining_expected_monsoon_inflow = 0
        # self.remaining_expected_non_monsoon_inflow = 0
        # self.remaining_expected_monsoon_outflow = 0
        # self.remaining_expected_non_monsoon_outflow = 0
        # self.actual_monsoon_inflow = 0
        # self.actual_monsoon_outflow = 0
        # self.actual_non_monsoon_inflow = 0
        # self.actual_non_monsoon_outflow = 0
        self.expected_monsoon_inflow = 0
        self.expected_non_monsoon_inflow = 0
        self.expected_monsoon_outflow = 0
        self.expected_non_monsoon_outflow = 0
        self.normalizing_factor = 0

        self.weather_df = pd.read_csv('dataset/Weather/mysuru_kodagu_hassan_weather.csv')
        self.inflow_df = pd.read_csv('dataset/reservoir_dataset_augmented.csv')
        self.inflow_df = self.inflow_df[self.inflow_df['RESERVOIR'] == 'K.R.S']
        self.season_df = self.inflow_df[['MONTH', 'DATE', 'SEASON']].drop_duplicates()
        self.normal_inflow_outflow_df = pd.read_csv('dataset/datewise_normal_inflow_outflow.csv')
        # self.normal_inflow_outflow_df = pd.read_csv('dataset/datewise_normal_inflow_outflow.csv')

        # Load encoders
        with open('training/KRS/encoders/month_le.pkl', 'rb') as f:
            self.month_le = pickle.load(f)
        with open('training/KRS/encoders/date_le.pkl', 'rb') as f:
            self.date_le = pickle.load(f)
        with open('training/KRS/encoders/season_le.pkl', 'rb') as f:
            self.season_le = pickle.load(f)
        
        with open('training/KRS/encoders/rs_inflow.pkl', 'rb') as f:
            self.rs_inflow = pickle.load(f)
        with open('training/KRS/encoders/rs_outflow.pkl', 'rb') as f:
            self.rs_outflow = pickle.load(f)
        with open('training/KRS/encoders/rs_temp.pkl', 'rb') as f:
            self.rs_temp = pickle.load(f)
        with open('training/KRS/encoders/rs_feels_like.pkl', 'rb') as f:
            self.rs_feels_like = pickle.load(f)
        with open('training/KRS/encoders/rs_temp_min.pkl', 'rb') as f:
            self.rs_temp_min = pickle.load(f)
        with open('training/KRS/encoders/rs_temp_max.pkl', 'rb') as f:
            self.rs_temp_max = pickle.load(f)
        with open('training/KRS/encoders/rs_pressure.pkl', 'rb') as f:
            self.rs_pressure = pickle.load(f)
        with open('training/KRS/encoders/rs_humidity.pkl', 'rb') as f:
            self.rs_humidity = pickle.load(f)
        with open('training/KRS/encoders/rs_wind_speed.pkl', 'rb') as f:
            self.rs_wind_speed = pickle.load(f)
        with open('training/KRS/encoders/rs_wind_deg.pkl', 'rb') as f:
            self.rs_wind_deg = pickle.load(f)
        with open('training/KRS/encoders/rs_rain.pkl', 'rb') as f:
            self.rs_rain = pickle.load(f)
        with open('training/KRS/encoders/rs_clouds_all.pkl', 'rb') as f:
            self.rs_clouds_all = pickle.load(f)

        # # weather data scaling
        # self.__apply_scaling(weather_df)

        # weather data district df
        self.kodagu_df = self.weather_df[self.weather_df['city_name'] == 'Kodagu'].reset_index(drop=True)
        self.hassan_df = self.weather_df[self.weather_df['city_name'] == 'Hassan'].reset_index(drop=True)
        self.mysuru_df = self.weather_df[self.weather_df['city_name'] == 'Mysuru'].reset_index(drop=True)

        # # create region-wise forecast df
        # start_date = datetime.date(year, 6, 1)
        # weather_available_date = start_date + datetime.timedelta(days=15)
        # self.mysuru_forecast_df, self.kodagu_forecast_df, self.hassan_forecast_df = self.__prepare_forecast_df(start_date, weather_available_date)
        # self.mysuru_forecast_df = self.mysuru_df.copy()
        # self.hassan_forecast_df = self.hassan_df.copy()
        # self.kodagu_forecast_df = self.kodagu_df.copy()

        self.mysuru_avg_df, self.kodagu_avg_df, self.hassan_avg_df = self.get_avg_weather_df(year)

        # region-wise weather data scaling
        self.__apply_scaling(self.kodagu_df)
        self.__apply_scaling(self.hassan_df)
        self.__apply_scaling(self.mysuru_df)
        self.__apply_scaling(self.kodagu_avg_df)
        self.__apply_scaling(self.hassan_avg_df)
        self.__apply_scaling(self.mysuru_avg_df)
        # self.__apply_scaling(self.kodagu_forecast_df)
        # self.__apply_scaling(self.hassan_forecast_df)
        # self.__apply_scaling(self.mysuru_forecast_df)

        self.__load_models()

        # create annual forecast
        prev_ddmmyyyy_list = [str(datetime.date(year, 6, 1) + datetime.timedelta(days=day)) for day in range(-10, 0)]
        if year == 2011:
            self.prediction_df = self.inflow_df[self.inflow_df['FLOW_DATE'].isin(prev_ddmmyyyy_list)]
            self.prediction_df['date'] = self.prediction_df['FLOW_DATE']
            self.prediction_df = self.prediction_df[['date', 'INFLOW_CUSECS', 'OUTFLOW_CUECS']]
            self.prediction_df.rename(columns={'INFLOW_CUSECS': 'ACTUAL INFLOW', 'OUTFLOW_CUECS': 'ACTUAL OUTFLOW'}, inplace=True)
            self.prediction_df['STORAGE'] = np.nan
            self.prediction_df['INFLOW'] = np.nan
            self.prediction_df['OUTFLOW'] = np.nan
            self.prediction_df['FORECAST'] = np.nan
            self.prediction_df['DURATION'] = np.nan
            # self.prediction_df['EXPECTED MONSOON INFLOW'] = np.nan
            # self.prediction_df['EXPECTED NON MONSOON INFLOW'] = np.nan
        # elif year == 2012:
        #     self.prediction_df = self.inflow_df[self.inflow_df['FLOW_DATE'].isin(prev_ddmmyyyy_list)]
        #     self.prediction_df['date'] = self.prediction_df['FLOW_DATE']
        #     self.prediction_df = self.prediction_df[['date', 'INFLOW_CUSECS', 'OUTFLOW_CUECS']]
        #     self.prediction_df.rename(columns={'INFLOW_CUSECS': 'ACTUAL INFLOW', 'OUTFLOW_CUECS': 'ACTUAL OUTFLOW'}, inplace=True)
        #     self.prediction_df['STORAGE'] = np.nan
        #     self.prediction_df['INFLOW'] = np.nan
        #     self.prediction_df['OUTFLOW'] = np.nan
        #     self.prediction_df['FORECAST'] = np.nan
        #     self.prediction_df['EXPECTED MONSOON INFLOW'] = np.nan
        #     self.prediction_df['EXPECTED NON MONSOON INFLOW'] = np.nan
        else:
            self.prediction_df = pd.read_json(f'predictions/KRS/predictions_{year-1}_{year}.json').reset_index()
            self.prediction_df.rename(columns={'index': 'date'}, inplace=True)
            self.prediction_df['date'] = self.prediction_df['date'].astype(str)
            self.prediction_df = self.prediction_df[self.prediction_df['date'].isin(prev_ddmmyyyy_list)]
        self.prediction_df.reset_index(drop=True, inplace=True)

        # self.prediction_df = {'INFLOW FORECAST' : {}, 'OUTFLOW FORECAST' : {}}
        # self.forecast(datetime.date(year, 6, 1))
        # with open('fr.pk', 'wb') as f:
        #     pickle.dump(self.annual_forecast, f)
        # with open('fr.pk', 'rb') as f:
        #     self.annual_forecast = pickle.load(f)
        # print(self.annual_forecast)
        # self.forecast(datetime.date(year+1, 5, 31))

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
        self.inflow_model = XGBoostModel('models/krs_inflow_xgboost.json')
        self.outflow_model = XGBoostModel('models/krs_outflow_xgboost.json')

    def __predict(self, loop_date, max_forecast_date, current_forecast_df=None):
        mysuru_df = self.mysuru_df#self.mysuru_forecast_df# if forecast else self.mysuru_df
        kodagu_df = self.kodagu_df#self.kodagu_forecast_df# if forecast else self.kodagu_df
        hassan_df = self.hassan_df#self.hassan_forecast_df# if forecast else self.hassan_df
        # kodagu_df = self.__apply_scaling(self.kodagu_df)
        # hassan_df = self.__apply_scaling(self.hassan_df)
        # mysuru_df = self.__apply_scaling(self.mysuru_df)

        # date_objs = str(loop_date).split('-')
        month = loop_date.month
        date = loop_date.day
        season = self.season_df[(self.season_df['DATE'] == date) & (self.season_df['MONTH'] == month)]['SEASON'].values[0]

        # prev_date_list = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, 1)]
        days_between_loop_date_max_forecast_date = (loop_date - max_forecast_date).days
        if days_between_loop_date_max_forecast_date < 1:
            prev_date_list = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, 1)]
            sel_kodagu = kodagu_df[kodagu_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()
            sel_hassan = hassan_df[hassan_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()
            sel_mysuru = mysuru_df[mysuru_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()
            # print('a', loop_date, max_forecast_date, sel_mysuru.shape)
        else:
            prev_actual_weather_dates = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, -days_between_loop_date_max_forecast_date+1)]
            prev_avg_weather_dates = [str(loop_date + datetime.timedelta(days=day)) for day in range(max(-days_between_loop_date_max_forecast_date+1, -10), 1)]

            kodagu_actual = kodagu_df[kodagu_df['date'].isin(prev_actual_weather_dates)].drop(columns=['date', 'city_name']).values.flatten()
            kodagu_avg = self.kodagu_avg_df[self.kodagu_avg_df['date'].isin(prev_avg_weather_dates)].drop(columns=['date', 'city_name']).values.flatten()
            sel_kodagu = np.concatenate([kodagu_actual, kodagu_avg])
            hassan_actual = hassan_df[hassan_df['date'].isin(prev_actual_weather_dates)].drop(columns=['date', 'city_name']).values.flatten()
            hassan_avg = self.hassan_avg_df[self.hassan_avg_df['date'].isin(prev_avg_weather_dates)].drop(columns=['date', 'city_name']).values.flatten()
            sel_hassan = np.concatenate([hassan_actual, hassan_avg])
            mysuru_actual = mysuru_df[mysuru_df['date'].isin(prev_actual_weather_dates)].drop(columns=['date', 'city_name']).values.flatten()
            mysuru_avg = self.mysuru_avg_df[self.mysuru_avg_df['date'].isin(prev_avg_weather_dates)].drop(columns=['date', 'city_name']).values.flatten()
            sel_mysuru = np.concatenate([mysuru_actual, mysuru_avg])
            # print(prev_actual_weather_dates, prev_avg_weather_dates)
            # print('b', loop_date, max_forecast_date, kodagu_avg.shape, hassan_avg.shape, mysuru_avg.shape)
            # print(self.mysuru_avg_df[self.mysuru_avg_df['date'].isin(prev_avg_weather_dates)][-3:])
            # if str(loop_date) == '2012-05-31':
            #     print(prev_actual_weather_dates, prev_avg_weather_dates)
            #     print('b', loop_date, max_forecast_date, sel_mysuru.shape, mysuru_actual.shape, mysuru_avg.shape)
            #     print(self.mysuru_avg_df[self.mysuru_avg_df['date'].isin(prev_avg_weather_dates)])
            # print('--------------')

        # if days_between_loop_date_max_forecast_date < 2:
        #     print('a')
        if current_forecast_df is not None:
            prev_inflow_dates = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, 0)]
            forecast_inflow_df = current_forecast_df[current_forecast_df['date'].isin(prev_inflow_dates)]
            missing_dates_in_forecast = set(prev_inflow_dates) - set(forecast_inflow_df['date'])
            forecast_inflow = forecast_inflow_df['INFLOW'].values.flatten()
            predicted_inflow = self.prediction_df[self.prediction_df['date'].isin(missing_dates_in_forecast)]['ACTUAL INFLOW'].values.flatten()
            sel_inflow = np.concatenate([predicted_inflow, forecast_inflow])
            # print(self.prediction_df[self.prediction_df['date'].isin(prev_inflow_dates)])
            # print(date, sel_inflow.shape, self.prediction_df)
            # sel_inflow = self.inflow_df[self.inflow_df['FLOW_DATE'].isin(prev_inflow_dates)]['INFLOW_CUSECS'].values.flatten()
        else:
            prev_inflow_dates = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, 0)]
            sel_inflow = self.prediction_df[self.prediction_df['date'].isin(prev_inflow_dates)]['ACTUAL INFLOW'].values.flatten()
        # print(sel_mysuru.shape, sel_inflow.shape)
        #     prev_actual_inflow_dates = [str(loop_date + datetime.timedelta(days=day)) for day in range(-10, -days_between_loop_date_max_forecast_date+1)]
        #     prev_pred_inflow_dates = [str(loop_date + datetime.timedelta(days=day)) for day in range(-days_between_loop_date_max_forecast_date+1, 0)]

        #     # actual_inflow = self.inflow_df[self.inflow_df['FLOW_DATE'].isin(prev_actual_inflow_dates)]['INFLOW_CUSECS'].values.flatten()
        #     actual_inflow = self.inflow_df[self.inflow_df['date'].isin(prev_actual_inflow_dates)]['ACTUAL INFLOW'].values.flatten()
        #     pred_inflow = current_forecast_df[current_forecast_df['date'].isin(prev_pred_inflow_dates)]['INFLOW'].values.flatten()
            
        #     # print(date, actual_inflow.shape, pred_inflow.shape)
        #     # print(current_forecast_df.shape)
        #     sel_inflow = np.concatenate([actual_inflow, pred_inflow])

        # sel_kodagu = kodagu_df[kodagu_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()
        # sel_hassan = hassan_df[hassan_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()
        # sel_mysuru = mysuru_df[mysuru_df['date'].isin(prev_date_list)].drop(columns=['date', 'city_name']).values.flatten()

        # if str(loop_date) in ['2011-06-01', '2011-06-02', '2011-06-03']:
        #     print(date, self.prediction_df[self.prediction_df['date'].isin(prev_ddmmyyyy_list)], prev_ddmmyyyy_list, sel_inflow.shape[0])
        #     print('----------------------')
        
        
        
        # if sel_inflow.shape[0] != len(prev_ddmmyyyy_list):
        #     raise Exception('Inflow shape mismatch')
        
        month_transformed = self.month_le.transform([month])
        date_transformed = self.date_le.transform([date])
        season_transformed = self.season_le.transform([season])
        # print(sel_mysuru.shape, sel_inflow.shape)

        inflow_prediction_input = np.concatenate([month_transformed, date_transformed, season_transformed, sel_mysuru, sel_kodagu, sel_hassan, self.rs_inflow.transform([sel_inflow])[0]]).reshape(1, -1)
        # print(inflow_prediction_input)
        # print(loop_date)
        # print(inflow_prediction_input.shape, sel_hassan.shape, sel_kodagu.shape, sel_mysuru.shape)

        y_hat_inflow = self.inflow_model(inflow_prediction_input)
        y_hat_inflow = self.rs_inflow.inverse_transform([[y_hat_inflow.item()]])[0][0]
        y_hat_inflow = round(y_hat_inflow) if y_hat_inflow > 0 else 0
        # y_hat_inflow = min(y_hat_inflow, 30000)
        # print(y_hat_inflow)

        outflow_prediction_input = np.concatenate([month_transformed, date_transformed, season_transformed, sel_mysuru, self.rs_inflow.transform([sel_inflow])[0], self.rs_inflow.transform([[y_hat_inflow]])[0]]).reshape(1, -1)
        y_hat_outflow = self.outflow_model(outflow_prediction_input)
        y_hat_outflow = self.rs_outflow.inverse_transform([[y_hat_outflow.item()]])[0][0]
        y_hat_outflow = round(y_hat_outflow)# + self.normalizing_factor)
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
    
    def get_avg_weather_df(self, year):
        # weather_forecast_available_end_date = weather_forecast_availibility_date
        # weather_forecast_unavailable_start_date = weather_forecast_available_end_date + datetime.timedelta(days=1)
        # weather_forecast_unavailable_end_date = checkpoint_date

        # weather_forecast_available_date_list = pd.date_range(date, weather_forecast_available_end_date, freq='d').astype(str)
        # forecast_df_start_date = date - datetime.timedelta(days=10)
        # forecast_df_end_date = self.cycle_end_date
        # weather_forecast_date_list = pd.date_range(, pd, freq='d')
        date = datetime.date(year, 6, 1)

        kodagu_df_tmp = self.weather_df[self.weather_df['city_name'] == 'Kodagu'].reset_index(drop=True)
        hassan_df_tmp = self.weather_df[self.weather_df['city_name'] == 'Hassan'].reset_index(drop=True)
        mysuru_df_tmp = self.weather_df[self.weather_df['city_name'] == 'Mysuru'].reset_index(drop=True)
        # mysuru1 = mysuru_df_tmp[mysuru_df_tmp['date'].isin(weather_forecast_available_date_list)]
        mysuru_df_tmp['YYYY'] = mysuru_df_tmp['date'].str[:4].astype(int)
        mysuru_df_tmp['MM'] = mysuru_df_tmp['date'].str[5:7].astype(int)
        mysuru_df_tmp['DD'] = mysuru_df_tmp['date'].str[8:].astype(int)

        # kodagu1 = kodagu_df_tmp[kodagu_df_tmp['date'].isin(weather_forecast_available_date_list)]
        kodagu_df_tmp['YYYY'] = kodagu_df_tmp['date'].str[:4].astype(int)
        kodagu_df_tmp['MM'] = kodagu_df_tmp['date'].str[5:7].astype(int)
        kodagu_df_tmp['DD'] = kodagu_df_tmp['date'].str[8:].astype(int)

        # hassan1 = hassan_df_tmp[hassan_df_tmp['date'].isin(weather_forecast_available_date_list)]
        hassan_df_tmp['YYYY'] = hassan_df_tmp['date'].str[:4].astype(int)
        hassan_df_tmp['MM'] = hassan_df_tmp['date'].str[5:7].astype(int)
        hassan_df_tmp['DD'] = hassan_df_tmp['date'].str[8:].astype(int)
        
        mysuru = []
        kodagu = []
        hassan = []
        delta = datetime.timedelta(days=1)
        while date <= self.cycle_end_date:
            yyyymmdd_str = str(date).split()[0]
            yyyy = int(yyyymmdd_str.split('-')[0])
            mm = int(yyyymmdd_str.split('-')[1])
            dd = int(yyyymmdd_str.split('-')[2])

            if mm == 2 and dd == 29:
                mysuru.append([yyyymmdd_str] + ['mysuru'] + mysuru_df_tmp[(mysuru_df_tmp['YYYY'] < yyyy) & (mysuru_df_tmp['MM'] == mm) & (mysuru_df_tmp['DD'].isin([dd-1, dd, dd+1]))].drop(columns=['date', 'city_name', 'YYYY', 'MM', 'DD']).mean().values.tolist())
                kodagu.append([yyyymmdd_str] + ['kodagu'] + kodagu_df_tmp[(kodagu_df_tmp['YYYY'] < yyyy) & (kodagu_df_tmp['MM'] == mm) & (kodagu_df_tmp['DD'].isin([dd-1, dd, dd+1]))].drop(columns=['date', 'city_name', 'YYYY', 'MM', 'DD']).mean().values.tolist())
                hassan.append([yyyymmdd_str] + ['hassan'] + hassan_df_tmp[(hassan_df_tmp['YYYY'] < yyyy) & (hassan_df_tmp['MM'] == mm) & (hassan_df_tmp['DD'].isin([dd-1, dd, dd+1]))].drop(columns=['date', 'city_name', 'YYYY', 'MM', 'DD']).mean().values.tolist())
            else:
                mysuru.append([yyyymmdd_str] + ['mysuru'] + mysuru_df_tmp[(mysuru_df_tmp['YYYY'] < yyyy) & (mysuru_df_tmp['MM'] == mm) & (mysuru_df_tmp['DD'] == dd)].drop(columns=['date', 'city_name', 'YYYY', 'MM', 'DD']).mean().values.tolist())
                kodagu.append([yyyymmdd_str] + ['kodagu'] + kodagu_df_tmp[(kodagu_df_tmp['YYYY'] < yyyy) & (kodagu_df_tmp['MM'] == mm) & (kodagu_df_tmp['DD'] == dd)].drop(columns=['date', 'city_name', 'YYYY', 'MM', 'DD']).mean().values.tolist())
                hassan.append([yyyymmdd_str] + ['hassan'] + hassan_df_tmp[(hassan_df_tmp['YYYY'] < yyyy) & (hassan_df_tmp['MM'] == mm) & (hassan_df_tmp['DD'] == dd)].drop(columns=['date', 'city_name', 'YYYY', 'MM', 'DD']).mean().values.tolist())
            # print(mysuru)

            date += delta

        columns = self.mysuru_df.columns
        mysuru_avg_df = pd.DataFrame(mysuru, columns=columns)
        kodagu_avg_df = pd.DataFrame(kodagu, columns=columns)
        hassan_avg_df = pd.DataFrame(hassan, columns=columns)
        # print(mysuru_forecast_df[mysuru_forecast_df.isnull().any(axis=1)])

        return mysuru_avg_df, kodagu_avg_df, hassan_avg_df

    def forecast(self, start_date, max_forecast_date):
        date = start_date# + datetime.timedelta(days=1)
        # actual_predict_date = date + datetime.timedelta(days=26)
        # self.remaining_expected_monsoon_inflow = 0
        # self.remaining_expected_non_monsoon_inflow = 0
        # self.remaining_expected_monsoon_outflow = 0
        # self.remaining_expected_non_monsoon_outflow = 0
        forecast_df = pd.DataFrame(columns=['date', 'INFLOW', 'OUTFLOW'])
        # else:
        #     if date.month >= 6:
        #         target_end_date = datetime.date(date.year, 12, 31)
        #     else:
        #         target_end_date = datetime.date(date.year, 5, 31)
        # forecast = {}
        
        delta = datetime.timedelta(days=1)
        while date <= self.cycle_end_date:
            # print(date, target_end_date)
            inflow, outflow = self.__predict(date, max_forecast_date, forecast_df)

            # index = self.prediction_df[self.prediction_df['date'].astype(str) == str(date)].index
            # forecast[str(date)] = {'INFLOW': inflow, 'OUTFLOW': outflow}
            # print(type(self.prediction_df['date']))
            # if len(index) == 0:
            index = forecast_df.shape[0]
            forecast_df.loc[index, 'date'] = str(date)
            forecast_df.loc[index, 'INFLOW'] = inflow
            forecast_df.loc[index, 'OUTFLOW'] = outflow
            # self.prediction_df['INFLOW FORECAST'].update({f'{formatted_date}': inflow})
            # self.annual_forecast['OUTFLOW FORECAST'].update({f'{formatted_date}': outflow})

        #     if date.month < 6:
        #         # print(date, inflow, outflow)
        #         self.remaining_expected_non_monsoon_inflow += inflow
        #         self.remaining_expected_non_monsoon_outflow += outflow
        #     else:
        #         self.remaining_expected_monsoon_inflow += inflow
        #         self.remaining_expected_monsoon_outflow += outflow

            date += delta
        
        # if loop_date.month >= 6:
        #     self.total_expected_monsoon_inflow = self.cum_inflow_till_prev_day + inflow + self.remaining_expected_monsoon_inflow
        #     self.total_expected_monsoon_outflow = self.cum_outflow_till_prev_day + outflow + self.remaining_expected_monsoon_outflow
        #     self.total_expected_non_monsoon_inflow = self.remaining_expected_non_monsoon_inflow
        #     self.total_expected_non_monsoon_outflow = self.remaining_expected_non_monsoon_outflow
        #     self.actual_monsoon_inflow = self.cum_inflow_till_prev_day
        #     self.actual_monsoon_outflow = self.cum_outflow_till_prev_day
        #     self.actual_non_monsoon_inflow = 0
        #     self.actual_non_monsoon_outflow = 0
        # else:
        #     # self.total_expected_monsoon_inflow = self.cum_inflow_till_prev_day + inflow + self.remaining_expected_monsoon_inflow
        #     # self.total_expected_monsoon_outflow = self.cum_outflow_till_prev_day + outflow + self.remaining_expected_monsoon_outflow
        #     if str(loop_date).endswith('01-01'):
        #         self.actual_monsoon_inflow = self.cum_inflow_till_prev_day
        #         self.actual_monsoon_outflow = self.cum_outflow_till_prev_day
        #         self.actual_non_monsoon_inflow = 0
        #         self.actual_non_monsoon_outflow = 0
        #     else:
        #         self.actual_non_monsoon_inflow = self.cum_inflow_till_prev_day - self.actual_monsoon_inflow
        #         self.actual_non_monsoon_outflow = self.cum_outflow_till_prev_day - self.actual_non_monsoon_outflow

        #     self.total_expected_non_monsoon_inflow = self.cum_inflow_till_prev_day + inflow + self.remaining_expected_non_monsoon_inflow - self.actual_monsoon_inflow
        #     self.total_expected_non_monsoon_outflow = self.cum_outflow_till_prev_day + outflow + self.remaining_expected_non_monsoon_outflow - self.actual_monsoon_outflow
        
        # import matplotlib.pyplot as plt
        # t = self.inflow_df.copy()
        # t.set_index('FLOW_DATE', inplace=True)
        # self.prediction_df['OUTFLOW'].plot()
        # t['OUTFLOW_CUECS'].plot()
        # plt.show(block=True)
        # plt.pause()

        #expected inflow
        self.expected_monsoon_inflow = forecast_df[(pd.to_datetime(forecast_df['date']) <= pd.Timestamp(self.cycle_end_date.year-1, 12, 31)) & (pd.to_datetime(forecast_df['date']) > pd.Timestamp(self.cycle_end_date.year-1, 5, 31))]['INFLOW'].sum() + \
            self.prediction_df[(pd.to_datetime(self.prediction_df['date']) <= pd.Timestamp(self.cycle_end_date.year-1, 12, 31)) & (pd.to_datetime(self.prediction_df['date']) > pd.Timestamp(self.cycle_end_date.year-1, 5, 31))]['INFLOW'].sum()
        self.expected_non_monsoon_inflow = forecast_df[(pd.to_datetime(forecast_df['date']) <= pd.Timestamp(self.cycle_end_date.year, 5, 31)) & (pd.to_datetime(forecast_df['date']) >= pd.Timestamp(self.cycle_end_date.year, 1, 1))]['INFLOW'].sum() + \
            self.prediction_df[(pd.to_datetime(self.prediction_df['date']) <= pd.Timestamp(self.cycle_end_date.year, 5, 31)) & (pd.to_datetime(self.prediction_df['date']) >= pd.Timestamp(self.cycle_end_date.year, 1, 1))]['INFLOW'].sum()
        

        # expected outflow
        self.expected_monsoon_outflow = forecast_df[(pd.to_datetime(forecast_df['date']) <= pd.Timestamp(self.cycle_end_date.year-1, 12, 31)) & (pd.to_datetime(forecast_df['date']) > pd.Timestamp(self.cycle_end_date.year-1, 5, 31))]['OUTFLOW'].sum() + \
            self.prediction_df[(pd.to_datetime(self.prediction_df['date']) <= pd.Timestamp(self.cycle_end_date.year-1, 12, 31)) & (pd.to_datetime(self.prediction_df['date']) > pd.Timestamp(self.cycle_end_date.year-1, 5, 31))]['OUTFLOW'].sum()
        self.expected_non_monsoon_outflow = forecast_df[(pd.to_datetime(forecast_df['date']) <= pd.Timestamp(self.cycle_end_date.year, 5, 31)) & (pd.to_datetime(forecast_df['date']) >= pd.Timestamp(self.cycle_end_date.year, 1, 1))]['OUTFLOW'].sum() + \
            self.prediction_df[(pd.to_datetime(self.prediction_df['date']) <= pd.Timestamp(self.cycle_end_date.year, 5, 31)) & (pd.to_datetime(self.prediction_df['date']) >= pd.Timestamp(self.cycle_end_date.year, 1, 1))]['OUTFLOW'].sum()
        # forecast_df['date'] = forecast_df['date'].astype(str)
        forecast_df.set_index('date', inplace=True)
        return forecast_df.to_dict()

    def set_normalizing_factor(self, normalizing_factor):
        self.normalizing_factor = normalizing_factor
    
    def __get_reservoir_duration(self, loop_date, storage, index):
        ndays = 0
        delta = datetime.timedelta(days=1)
        date = loop_date
        roll_year = False
        while storage > 0:
            if date.month == 5 and date.day == 31:
                date = datetime.date(date.year-1, 5, 31)
                roll_year = True
            
            ndays += 1
            date += delta
            # formatted_date = date.strftime('%d-%m-%Y')

            if not roll_year:
                outflow = self.prediction_df.loc[index, 'FORECAST']['OUTFLOW'][str(date)]
            else:
                outflow = self.prediction_df[self.prediction_df['date'] == str(date)]['OUTFLOW'].values[0]
            outflow_tmc = 8.64e-05 * outflow
            storage -= outflow_tmc
        
        if ndays > 152:
            return '> 150'
            if idx + ndays in self.pred_df.index:
                outflow = float(self.pred_df.loc[idx+ndays, ('OUTFLOW')])
            else:
                ddmm = f'{date}-{month}'
                ddmmyyyy = f'{ddmm}-{self.start_year}'
                outflow = self.all_amcs_outflow_df.loc[ddmm].tolist() if self.all_amcs_outflow_df is not None else []
                outflow += self.pred_df[self.pred_df['DD-MM-YYYY'] == ddmmyyyy]['OUTFLOW'].tolist()
                outflow = sum(outflow) / len(outflow)
                
                if (month in [6, 9, 11] and date == 30) or (month in [7, 8, 10, 12] and date == 31):
                    month += 1
                    date = 1
            outflow_tmc = 8.64e-05 * outflow
            storage -= outflow_tmc
            
            if ndays > 152:
                return '> 150'
        
        return max(ndays - 1, 0)

    def predict_and_forecast(self, loop_date):
        
        # update forecast df
        
        # print(self.mysuru_forecast_df.shape)
        # print(self.mysuru_forecast_df['date'].unique())
        # self.mysuru_forecast_df = pd.concat([self.mysuru_forecast_df,mysuru_available_forecast_df]).drop_duplicates(['date'],keep='last')
        # print(self.mysuru_forecast_df.shape)
        # self.mysuru_forecast_df['date'] = pd.to_datetime(self.mysuru_forecast_df.date).dt.date.astype(str)
        # self.mysuru_forecast_df.sort_values(by='date', inplace=True)

        # self.kodagu_forecast_df = pd.concat([self.kodagu_forecast_df,kodagu_available_forecast_df]).drop_duplicates(['date'],keep='last')
        # self.kodagu_forecast_df['date'] = pd.to_datetime(self.kodagu_forecast_df.date).dt.date.astype(str)
        # self.kodagu_forecast_df.sort_values(by='date', inplace=True)

        # self.hassan_forecast_df = pd.concat([self.hassan_forecast_df,hassan_available_forecast_df]).drop_duplicates(['date'],keep='last')
        # self.hassan_forecast_df['date'] = pd.to_datetime(self.hassan_forecast_df.date).dt.date.astype(str)
        # self.hassan_forecast_df.sort_values(by='date', inplace=True)

        #predict
        result_dict = {}
        inflow, outflow = self.__predict(loop_date, max_forecast_date=loop_date + datetime.timedelta(days=15))
        
        # for debugging
        if np.isnan(outflow):
            print(loop_date)

        actual_data = self.inflow_df[(self.inflow_df['YEAR'] == loop_date.year) &
                                     (self.inflow_df['MONTH'] == loop_date.month) &
                                     (self.inflow_df['DATE'] == loop_date.day)]
        actual_inflow = actual_data['INFLOW_CUSECS'].values[0]# if actual_data['DAY'] == np.nan else inflow
        storage, non_amcs_outflow = self.__get_storage(actual_inflow, outflow, self.curr_non_amcs_storage)
        self.curr_non_amcs_storage = round(storage, 2)
        # print(actual_data['DAY'].values[0], np.isnan(actual_data['DAY'].values[0]), np.nan)#, actual_data['DAY'].isna())
        actual_outflow = actual_data['OUTFLOW_CUECS'].values[0] if not np.isnan(actual_data['DAY'].values[0]) else non_amcs_outflow
        normal_outflow = self.normal_inflow_outflow_df[self.normal_inflow_outflow_df['MONTH_DATE'] == f'{str(loop_date)[5:]}']['OUTFLOW_CUECS'].values[0]
        normal_inflow = self.normal_inflow_outflow_df[self.normal_inflow_outflow_df['MONTH_DATE'] == f'{str(loop_date)[5:]}']['INFLOW_CUSECS'].values[0]
        

        # prev_date = loop_date - datetime.timedelta(days=1)
        # normal_inflow_prev_day = self.normal_inflow_outflow_df[(self.normal_inflow_outflow_df['MONTH'] == prev_date.month) &
        #                                                        (self.normal_inflow_outflow_df['DATE'] == prev_date.day)]['INFLOW_CUSECS'].mean()
        # duration = self.__get_reservoir_duration(loop_date, self.curr_amcs_storage)

        formatted_date = re.sub('0(\d-)', '\g<1>', str(loop_date.strftime('%d-%m-%Y')))
        index = self.prediction_df[self.prediction_df['date'].astype(str) == str(loop_date)].index
        # print(type(self.prediction_df['date']))
        if len(index) == 0:
            index = self.prediction_df.shape[0]
            self.prediction_df.loc[index, 'date'] = str(loop_date)
        self.prediction_df.loc[index, 'ACTUAL INFLOW'] = actual_inflow
        # print(type(index))
        self.prediction_df.loc[index, 'ACTUAL OUTFLOW'] = actual_outflow
        self.prediction_df.loc[index, 'NORMAL OUTFLOW'] = normal_outflow
        self.prediction_df.loc[index, 'NORMAL INFLOW'] = normal_inflow
        self.prediction_df.loc[index, 'INFLOW'] = inflow
        self.prediction_df.loc[index, 'OUTFLOW'] = non_amcs_outflow
        self.prediction_df.loc[index, 'STORAGE'] = self.curr_non_amcs_storage
        # get amcs outflow
        amcs_outflow = max(outflow + self.normalizing_factor, 0)
        storage, amcs_outflow = self.__get_storage(actual_inflow, amcs_outflow, self.curr_amcs_storage)
        self.prediction_df.loc[index, 'AMCS OUTFLOW'] = amcs_outflow
        self.curr_amcs_storage = round(storage, 2)
        self.prediction_df.loc[index, 'AMCS STORAGE'] = self.curr_amcs_storage
        # self.prediction_df.loc[index, 'DURATION'] = duration
        # result_dict['INFLOW'] = {f'{formatted_date}': inflow}
        # result_dict['AMCS OUTFLOW'] = {f'{formatted_date}': outflow}
        # # result_dict['AMCS STORAGE'] = {f'{formatted_date}': self.curr_amcs_storage}
        # result_dict['ACTUAL INFLOW'] = {f'{formatted_date}': actual_inflow}
        # result_dict['ACTUAL OUTFLOW'] = {f'{formatted_date}': actual_outflow}
        # # result_dict['DURATION'] = {f'{formatted_date}': duration}

        # if prev_date == datetime.date(loop_date.year, 5, 31):
        #     self.cum_inflow_till_prev_day = 0
        #     self.cum_outflow_till_prev_day = 0
        #     self.normal_cum_inflow_till_prev_day = 0
        # else:
        #     self.cum_inflow_till_prev_day += actual_inflow
        #     self.cum_outflow_till_prev_day += amcs_outflow
        #     self.normal_cum_inflow_till_prev_day += normal_inflow_prev_day
        

        # weather_forecast_availibility_date = loop_date + datetime.timedelta(days=16)
        # # cycle_end_year = loop_date.year if loop_date.month < 6 else loop_date.year + 1
        # # cycle_end_date = datetime.date(cycle_end_year, 5, 31)
        # self.mysuru_forecast_df, self.kodagu_forecast_df, self.hassan_forecast_df = self.__prepare_forecast_df(loop_date, weather_forecast_availibility_date)
        
        # self.__apply_scaling(self.mysuru_forecast_df)
        # self.__apply_scaling(self.kodagu_forecast_df)
        # self.__apply_scaling(self.hassan_forecast_df)
        forecast_start_date = loop_date + datetime.timedelta(days=1)
        self.prediction_df.loc[index, 'FORECAST'] = [self.forecast(forecast_start_date, max_forecast_date=forecast_start_date + datetime.timedelta(days=15))]
        duration = self.__get_reservoir_duration(loop_date, self.curr_amcs_storage, index)
        self.prediction_df.loc[index, 'DURATION'] = duration
        # self.prediction_df.loc[index, 'EXPECTED MONSOON INFLOW'] = self.expected_monsoon_rainfall
        # self.prediction_df.loc[index, 'EXPECTED NON MONSOON INFLOW'] = self.expected_non_monsoon_rainfall
        
        return result_dict
    
    def get_current_storage(self):
        return self.curr_amcs_storage
    
    def get_expected_monsoon_inflow_outflow(self):
        return self.expected_monsoon_inflow, self.expected_monsoon_outflow

    def get_expected_non_monsoon_inflow_outflow(self):
        return self.expected_non_monsoon_inflow, self.expected_non_monsoon_outflow
    
    # def get_cum_inflow_till_prev_day(self):
    #     return self.cum_inflow_till_prev_day
    
    # def get_normal_inflow_till_prev_day(self):
    #     return self.normal_cum_inflow_till_prev_day
    
    def get_max_storage(self):
        return self.max_storage

    def trim_df_top(self):
        self.prediction_df = self.prediction_df[pd.to_datetime(self.prediction_df['date']) > pd.Timestamp(self.cycle_end_date.year-1, self.cycle_end_date.month, self.cycle_end_date.day)]