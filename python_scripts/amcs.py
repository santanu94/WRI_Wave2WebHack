import datetime
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

class AMCS:
    def __init__(self, reservoir_obj, year) -> None:
        self.reservoir_obj = reservoir_obj
        # self.expected_monsoon_inflow_tmc = 342
        # self.expected_non_monsoon_inflow_tmc = 12

        self.drought = 'noDrought'

        self.normal_inflow_outflow_df = pd.read_csv('dataset/datewise_normal_inflow_outflow.csv')
    
    def _get_updated_storage_profile(self):
        max_capacity = self.reservoir_obj.get_max_storage()
        if self.drought == 'noDrought':
            return {'monsoon_end_storage_target': 0.9 * max_capacity,
                    'cycle_end_storage_target': 0.3 * max_capacity}
        elif self.drought == 'Slight':
            return {'monsoon_end_storage_target': 0.4 * max_capacity,
                    'cycle_end_storage_target': 0.1 * max_capacity}
        elif self.drought == 'Moderate':
            return {'monsoon_end_storage_target': 0.3 * max_capacity,
                    'cycle_end_storage_target': 0 * max_capacity}
        elif self.drought == 'Severe':
            return {'monsoon_end_storage_target': 0.2 * max_capacity,
                    'cycle_end_storage_target': 0 * max_capacity}
    # def __init__(self, model_prediction, reservoir, total_capacity, start_year, end_year):
    #     self.start_year = start_year
    #     self.total_capacity = total_capacity
    #     self.drought = False
    #     self.__get_pred_df(model_prediction)
    #     self.__load_inflow_df(reservoir, start_year, end_year)
    #     self.__load_all_actual_inflow_df(reservoir, start_year)
    #     self.__load_all_amcs_outflow_df(reservoir, start_year)

    #     self.deviation = [0] * self.pred_df.shape[0]
    #     self.model_predicted_outflow = self.pred_df['OUTFLOW'].tolist()
    
    # def __get_pred_df(self, model_prediction):
    #     self.pred_df = pd.DataFrame(model_prediction).reset_index()
    #     self.pred_df.rename(columns={'index': 'DD-MM-YYYY'}, inplace=True)
    #     self.pred_df['YEAR'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[2].astype(int)
    #     self.pred_df['MONTH'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[1].astype(int)
    #     self.pred_df['DATE'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[0].astype(int)
    #     self.pred_df = self.pred_df.sort_values(['YEAR', 'MONTH', 'DATE']).reset_index(drop=True)
    #     self.pred_df['INTERVAL'] = self.__get_interval_column(self.pred_df)
    #     self.pred_df['SEASON'] = self.__get_season(self.pred_df['MONTH'])

    # def __load_inflow_df(self, reservoir, start_year, end_year):
    #     self.inflow_df = pd.read_csv('dataset/reservoir_dataset.csv')
    #     self.inflow_df = self.inflow_df[self.inflow_df['RESERVOIR'] == reservoir]
    #     inflow_df_1 = self.inflow_df[(self.inflow_df['MONTH'] < 6) & (self.inflow_df['YEAR'] == end_year)]
    #     inflow_df_2 = self.inflow_df[(self.inflow_df['MONTH'] >= 6) & (self.inflow_df['YEAR'] == start_year)]
    #     self.inflow_df = inflow_df_1.append(inflow_df_2, ignore_index=True)
    #     self.inflow_df['DD-MM-YYYY'] = self.inflow_df['DATE'].astype(str) + '-' + self.inflow_df['MONTH'].astype(str) + '-' + self.inflow_df['YEAR'].astype(str)
    #     self.__fill_missing_actual_inflow_outflow()
    #     self.inflow_df = self.inflow_df.sort_values(['YEAR', 'MONTH', 'DATE']).reset_index(drop=True)
    #     self.inflow_df['INTERVAL'] = self.__get_interval_column(self.inflow_df)
    #     self.inflow_df['SEASON'] = self.__get_season(self.inflow_df['MONTH'])

    # def __load_all_actual_inflow_df(self, reservoir, start_year):
    #     try:
    #         if start_year > 2011:
    #             reservoir = reservoir.replace('.', '')
    #             self.all_actual_inflow_df = pd.read_csv(f'predictions/{reservoir}/all_actual_inflow.csv', index_col=0)
    #             self.all_actual_inflow_df = self.all_actual_inflow_df[self.all_actual_inflow_df.columns[self.all_actual_inflow_df.columns.str.split('-').str[0].astype(int) < start_year]]                
    #         else:
    #             self.all_actual_inflow_df = None
    #     except FileNotFoundError:
    #         self.all_actual_inflow_df = None
    
    # def __load_all_amcs_outflow_df(self, reservoir, start_year):
    #     try:
    #         if start_year > 2011:
    #             reservoir = reservoir.replace('.', '')
    #             self.all_amcs_outflow_df = pd.read_csv(f'predictions/{reservoir}/all_amcs_outflow.csv', index_col=0)
    #             self.all_amcs_outflow_df = self.all_amcs_outflow_df[self.all_amcs_outflow_df.columns[self.all_amcs_outflow_df.columns.str.split('-').str[0].astype(int) < start_year]]                
    #         else:
    #             self.all_amcs_outflow_df = None
    #     except FileNotFoundError:
    #         self.all_amcs_outflow_df = None
    
    # def __fill_missing_actual_inflow_outflow(self):
    #     date = []
    #     inflow_cusecs = []
    #     outflow_cusecs = []
    #     year = []
    #     month = []
    #     timestamp = []
    #     for ddmmyyyy, inflow, outflow in self.pred_df[['DD-MM-YYYY', 'INFLOW', 'OUTFLOW']].values:
    #         if ddmmyyyy not in self.inflow_df['DD-MM-YYYY'].unique():
    #             dd, mm, yyyy = ddmmyyyy.split('-')
    #             timestamp.append(ddmmyyyy)
    #             inflow_cusecs.append(inflow)
    #             outflow_cusecs.append(outflow)
    #             date.append(int(dd))
    #             month.append(int(mm))
    #             year.append(int(yyyy))
        
    #     self.inflow_df = self.inflow_df.append(pd.DataFrame({'DD-MM-YYYY': timestamp,
    #                                                          'INFLOW_CUSECS': inflow_cusecs,
    #                                                          'OUTFLOW_CUECS': outflow_cusecs,
    #                                                          'DATE': date,
    #                                                          'MONTH': month,
    #                                                          'YEAR': year}), ignore_index=True)

    # def __get_interval_column(self, df):
    #     interval_col = []
    #     month_list = [6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]
    #     for idx, row in df.iterrows():
    #         date = row['DATE']
    #         interval = month_list.index(row['MONTH']) * 4
    #         if date >= 1 and date <= 7:
    #             interval += 1
    #         elif date >= 8 and date <= 14:
    #             interval += 2
    #         elif date >= 15 and date <= 21:
    #             interval += 3
    #         else:
    #             interval += 4

    #         interval_col.append(interval)
    #     return interval_col

    # def __get_season(self, month_col):
    #     season_col = []
    #     season_month = {'WINTER': [1, 2],
    #                     'SUMMER': [3, 4, 5],
    #                     'MONSOON': [6, 7, 8, 9],
    #                     'POST-MONSOON': [10, 11, 12]
    #                    }
        
    #     for month in month_col.values:
    #         if month in season_month['WINTER']:
    #             season_col.append('WINTER')
    #         elif month in season_month['SUMMER']:
    #             season_col.append('SUMMER')
    #         elif month in season_month['MONSOON']:
    #             season_col.append('MONSOON')
    #         elif month in season_month['POST-MONSOON']:
    #             season_col.append('POST-MONSOON')
    #         else:
    #             raise Exception(f'Unknown month {month} in datestamp {ddmmyyyy}')
        
    #     return season_col
    
    # def __get_outflow(self, interval, storage, season):
    #     pred_remaining_df = self.pred_df[self.pred_df['INTERVAL'] > interval]
    #     pred_remaining_start_idx = pred_remaining_df.index[0]
    #     remaining_old_pred_outflow = pred_remaining_df['OUTFLOW'].values
    #     remaining_old_pred_outflow[remaining_old_pred_outflow == 0] = remaining_old_pred_outflow[remaining_old_pred_outflow != 0].mean() if remaining_old_pred_outflow.sum() > 0 else 0        
        
    #     expected_remaining_total_monsoon_inflow = self.pred_df[(self.pred_df['INTERVAL'] > interval) & (self.inflow_df['SEASON'].isin(['MONSOON', 'POST-MONSOON']))]['INFLOW'].sum()
    #     expected_remaining_total_non_monsoon_inflow = self.pred_df[(self.pred_df['INTERVAL'] > interval) & (self.inflow_df['SEASON'].isin(['WINTER', 'SUMMER']))]['INFLOW'].sum()
    #     expected_remaining_total_monsoon_tmc = 8.64e-05 * expected_remaining_total_monsoon_inflow
    #     expected_remaining_total_non_monsoon_tmc = 8.64e-05 * expected_remaining_total_non_monsoon_inflow

    #     if self.drought:
    #         if self.drought == 'Slight':
    #             monsoon_end_storage_threshold = self.total_capacity * 0.4
    #             year_end_threshold = self.total_capacity * 0.1
    #         elif self.drought == 'Moderate':
    #             monsoon_end_storage_threshold = self.total_capacity * 0.3
    #             year_end_threshold = self.total_capacity * 0
    #         elif self.drought == 'Severe':
    #             monsoon_end_storage_threshold = self.total_capacity * 0.2
    #             year_end_threshold = 0
            
    #         if season in ['MONSOON', 'POST-MONSOON']:
    #             # we calculate distribution of remaining weeks
    #             remaining_monsoon_df = pred_remaining_df[pred_remaining_df['SEASON'].isin(['MONSOON', 'POST-MONSOON'])]
    #             remaining_non_monsoon_df = pred_remaining_df[pred_remaining_df['SEASON'].isin(['WINTER', 'SUMMER'])]
    #             outflow_monsoon_dist = remaining_monsoon_df['OUTFLOW'].values / (remaining_monsoon_df['OUTFLOW'].sum() if remaining_monsoon_df['OUTFLOW'].sum() > 0 else 1)
    #             outflow_non_monsoon_dist = remaining_non_monsoon_df['OUTFLOW'].values / (remaining_non_monsoon_df['OUTFLOW'].sum() if remaining_non_monsoon_df['OUTFLOW'].sum() > 0 else 1)
                
    #             water_to_dispatch_monsoon_tmc = expected_remaining_total_monsoon_tmc + storage - monsoon_end_storage_threshold
    #             water_to_dispatch_non_monsoon_tmc = expected_remaining_total_non_monsoon_tmc + monsoon_end_storage_threshold - year_end_threshold

    #             new_outflow_list = np.append((outflow_monsoon_dist * water_to_dispatch_monsoon_tmc * 11574.074), (outflow_non_monsoon_dist * water_to_dispatch_non_monsoon_tmc * 11574.074))
    #         elif season in ['WINTER', 'SUMMER']:
    #             water_to_dispatch_tmc = expected_remaining_total_non_monsoon_tmc + storage - year_end_threshold

    #             # we calculate distribution of remaining weeks
    #             outflow_dist = remaining_old_pred_outflow / (remaining_old_pred_outflow.sum() if remaining_old_pred_outflow.sum() > 0 else 1)
    #             new_outflow_list = outflow_dist * water_to_dispatch_tmc * 11574.074
    #     else:
    #         if season in ['WINTER', 'SUMMER']:
    #             year_end_threshold = self.total_capacity * 0.3
    #             water_to_dispatch_tmc = expected_remaining_total_non_monsoon_tmc + storage - year_end_threshold

    #             # we calculate distribution of remaining weeks
    #             outflow_non_monsoon_dist = remaining_old_pred_outflow / (remaining_old_pred_outflow.sum() if remaining_old_pred_outflow.sum() > 0 else 1)
    #             new_outflow_list = outflow_non_monsoon_dist * water_to_dispatch_tmc * 11574.074
    #         elif season in ['MONSOON', 'POST-MONSOON']:
    #             remaining_monsoon_arr = pred_remaining_df[pred_remaining_df['SEASON'].isin(['MONSOON', 'POST-MONSOON'])]['OUTFLOW'].values
    #             remaining_non_monsoon_arr = pred_remaining_df[pred_remaining_df['SEASON'].isin(['WINTER', 'SUMMER'])]['OUTFLOW'].values

    #             remaining_non_monsoon_arr_mean = remaining_non_monsoon_arr[remaining_non_monsoon_arr > 0].mean()
    #             remaining_non_monsoon_arr[remaining_non_monsoon_arr < remaining_non_monsoon_arr_mean] = remaining_non_monsoon_arr_mean
                
    #             # we calculate distribution of remaining weeks
    #             outflow_monsoon_dist = remaining_monsoon_arr / (remaining_monsoon_arr.sum() if remaining_monsoon_arr.sum() > 0 else 1)
    #             outflow_non_monsoon_dist = remaining_non_monsoon_arr / (remaining_non_monsoon_arr.sum() if remaining_non_monsoon_arr.sum() > 0 else 1)

    #             water_to_dispatch_monsoon_tmc = expected_remaining_total_monsoon_tmc + storage - self.total_capacity * 0.9
    #             water_to_dispatch_non_monsoon_tmc = expected_remaining_total_non_monsoon_tmc + self.total_capacity * 0.6
    #             new_outflow_list = np.append((outflow_monsoon_dist * water_to_dispatch_monsoon_tmc * 11574.074), (outflow_non_monsoon_dist * water_to_dispatch_non_monsoon_tmc * 11574.074))
    #         else:
    #             raise Exception('Unknown season')
        
    #     new_outflow_list[new_outflow_list < 0] = 0
    #     self.pred_df.loc[pred_remaining_start_idx:, ('OUTFLOW')] = new_outflow_list.copy()

    def __drought_prediction(self, actual_inflow, normal_inflow):
        if actual_inflow < normal_inflow:
            inflow_deficiency = (normal_inflow - actual_inflow) * 100 / normal_inflow

            if inflow_deficiency > 10 and inflow_deficiency <= 25:
                self.drought = 'Slight'
            elif inflow_deficiency > 25 and inflow_deficiency <= 50:
                self.drought = 'Moderate'
            elif inflow_deficiency > 50:
                self.drought = 'Severe'
            else:
                self.drought = 'noDrought'
        else:
            self.drought = 'noDrought'
    
    # def __get_storage(self, inflow, outflow, storage):
    #     inflow_tmc = 8.64e-05 * inflow
    #     outflow_tmc = 8.64e-05 * outflow
    #     print(outflow, outflow_tmc)
    #     storage = storage + inflow_tmc
    #     if outflow_tmc > storage or storage == 0:
    #         outflow = 11574.074 * storage
    #         storage = 0
    #     else:
    #         storage -= outflow_tmc
        
    #     if storage > self.total_capacity:
    #         outflow += 11574.074 * (storage - self.total_capacity)
    #         storage = self.total_capacity
        
        
    #     storage_pct = storage * 100 / self.total_capacity
        
    #     return int(outflow), round(storage, 2), round(storage_pct, 1)
    
    
    
    def run(self, loop_date):
        curr_cycle_prediction_df = self.reservoir_obj.prediction_df[pd.to_datetime(self.reservoir_obj.prediction_df['date']) > pd.Timestamp(self.cycle_end_date.year-1, self.cycle_end_date.month, self.cycle_end_date.day)]
        curr_cycle_completed_month_date = curr_cycle_prediction_df['date'].str[5:]
        cum_normal_inflow = self.normal_inflow_outflow_df[self.normal_inflow_outflow_df['MONTH_DATE'].isin(curr_cycle_completed_month_date)]['INFLOW_CUSECS'].sum()
        # cum_normal_inflow = 0
        # for date in curr_cycle_prediction_df['date'].values:
        #     normal_inflow = self.normal_inflow_outflow_df[(self.normal_inflow_outflow_df['MONTH'] == date.month) &
        #                                                             (self.normal_inflow_outflow_df['DATE'] == date.day)]['INFLOW_CUSECS']
        #     cum_normal_inflow += normal_inflow
        cum_actual_inflow = curr_cycle_prediction_df['ACTUAL INFLOW'].sum()
        # print(cum_actual_inflow)
        # print(self.reservoir_obj.prediction_df[['date', 'ACTUAL INFLOW']])
        # cum_normal_inflow = self.reservoir_obj.get_normal_inflow_till_prev_day()

        if cum_actual_inflow == 0:
            self.cycle_start_storage = self.reservoir_obj.get_current_storage()
            return

        # self.reservoir_obj.forecast(loop_date)
        self.__drought_prediction(cum_actual_inflow, cum_normal_inflow)
        # print(loop_date, self.drought)
        storage_profile = self._get_updated_storage_profile()

        if loop_date.month >= 6:
            expected_monsoon_inflow_based_on_current_weather, expected_monsoon_outflow_based_on_current_weather = self.reservoir_obj.get_expected_monsoon_inflow_outflow()
            amcs_target_monsoon_outflow = expected_monsoon_inflow_based_on_current_weather + 11574.074 * (self.cycle_start_storage - storage_profile['monsoon_end_storage_target'])
            # amcs_target_monsoon_outflow = 11574.074 * amcs_target_monsoon_outflow_tmc
            # self.expected_monsoon_inflow_tmc
            # print(loop_date, 8.64e-05 * expected_monsoon_inflow_based_on_current_weather, 8.64e-05 * expected_monsoon_outflow_based_on_current_weather)

            expected_outflow_difference = amcs_target_monsoon_outflow - expected_monsoon_outflow_based_on_current_weather
            num_days_to_checkpoint = int(str(datetime.date(loop_date.year, 12, 31) - loop_date).split()[0])
            normalizing_factor = expected_outflow_difference / num_days_to_checkpoint

            self.reservoir_obj.set_normalizing_factor(normalizing_factor)
        else:
            expected_non_monsoon_inflow_based_on_current_weather, expected_non_monsoon_outflow_based_on_current_weather = self.reservoir_obj.get_expected_non_monsoon_inflow_outflow()
            amcs_target_non_monsoon_outflow = expected_non_monsoon_inflow_based_on_current_weather + 11574.074 * (storage_profile['monsoon_end_storage_target'] - storage_profile['cycle_end_storage_target'])
            # amcs_target_non_monsoon_outflow = 11574.074 * amcs_target_non_monsoon_outflow_tmc
            # print(loop_date, 8.64e-05 * expected_non_monsoon_inflow_based_on_current_weather, 8.64e-05 * expected_non_monsoon_outflow_based_on_current_weather)

            expected_outflow_difference = amcs_target_non_monsoon_outflow - expected_non_monsoon_outflow_based_on_current_weather
            num_days_to_checkpoint = int(str(datetime.date(loop_date.year+1, 5, 31) - loop_date).split()[0])
            normalizing_factor = expected_outflow_difference / num_days_to_checkpoint

            self.reservoir_obj.set_normalizing_factor(normalizing_factor)
        
    # def run(self, storage):
    #     amcs_outflow = {}
    #     self.pred_df.merge(self.inflow_df, on='DD-MM-YYYY')
    #     amcs_outflow['ACTUAL INFLOW'] = self.inflow_df[['DD-MM-YYYY', 'INFLOW_CUSECS']].set_index('DD-MM-YYYY')['INFLOW_CUSECS'].to_dict()
    #     amcs_outflow['ACTUAL OUTFLOW'] = self.inflow_df[['DD-MM-YYYY', 'OUTFLOW_CUECS']].set_index('DD-MM-YYYY')['OUTFLOW_CUECS'].to_dict()
    #     amcs_outflow['AMCS OUTFLOW'] = {}
    #     amcs_outflow['AMCS STORAGE'] = {}
    #     amcs_outflow['AMCS STORAGE PCT'] = {}
    #     amcs_outflow['NORMAL INFLOW'] = {}
    #     amcs_outflow['NORMAL OUTFLOW'] = {}
    #     amcs_outflow['DURATION'] = {}
    #     prev_interval = None
    #     cum_actual_inflow = 0
    #     cum_normal_inflow = 0
    #     for idx, row in self.pred_df.iterrows():
    #         interval = row['INTERVAL']
    #         season = row['SEASON']
    #         outflow = float(self.pred_df.loc[idx, ('OUTFLOW')])
    #         ddmmyyyy = row['DD-MM-YYYY']
    #         ddmm = '-'.join(ddmmyyyy.split('-')[:-1])
    #         actual_inflow = amcs_outflow['ACTUAL INFLOW'][ddmmyyyy]
    #         normal_inflow = self.all_actual_inflow_df.loc[ddmm].mean() if self.all_actual_inflow_df is not None else 0
    #         normal_outflow = self.all_amcs_outflow_df.loc[ddmm].mean() if self.all_amcs_outflow_df is not None else 0
            
    #         cum_actual_inflow += actual_inflow
    #         cum_normal_inflow += normal_inflow
    #         self.__drought_prediction(cum_actual_inflow, cum_normal_inflow)
            
    #         if interval > 1 and prev_interval != interval and interval < 48:
    #             self.__get_outflow(interval, storage, season)
    #             prev_interval = interval
            
    #         outflow, storage, storage_pct = self.__get_storage(actual_inflow, outflow, storage)
    #         duration = self.__get_reservoir_duration(storage, idx)
    #         amcs_outflow['AMCS OUTFLOW'][ddmmyyyy] = outflow
    #         amcs_outflow['AMCS STORAGE'][ddmmyyyy] = storage
    #         amcs_outflow['AMCS STORAGE PCT'][ddmmyyyy] = storage_pct
    #         amcs_outflow['NORMAL INFLOW'][ddmmyyyy] = normal_inflow
    #         amcs_outflow['NORMAL OUTFLOW'][ddmmyyyy] = normal_outflow
    #         amcs_outflow['DURATION'][ddmmyyyy] = duration

    #     return amcs_outflow