import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

class AMCS:
    def __init__(self, model_prediction, reservoir, total_capacity, start_year, end_year):
        self.start_year = start_year
        self.total_capacity = total_capacity
        self.drought = False
        self.__get_pred_df(model_prediction)
        self.__load_inflow_df(reservoir, start_year, end_year)
        self.__load_all_actual_inflow_df(reservoir, start_year)
        self.__load_all_amcs_outflow_df(reservoir, start_year)

        self.deviation = [0] * self.pred_df.shape[0]
        self.model_predicted_outflow = self.pred_df['OUTFLOW'].tolist()
    
    def __get_pred_df(self, model_prediction):
        self.pred_df = pd.DataFrame(model_prediction).reset_index()
        self.pred_df.rename(columns={'index': 'DD-MM-YYYY'}, inplace=True)
        self.pred_df['YEAR'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[2].astype(int)
        self.pred_df['MONTH'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[1].astype(int)
        self.pred_df['DATE'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[0].astype(int)
        self.pred_df = self.pred_df.sort_values(['YEAR', 'MONTH', 'DATE']).reset_index(drop=True)
        self.pred_df['INTERVAL'] = self.__get_interval_column(self.pred_df)
        self.pred_df['SEASON'] = self.__get_season(self.pred_df['MONTH'])

    def __load_inflow_df(self, reservoir, start_year, end_year):
        self.inflow_df = pd.read_csv('dataset/reservoir_dataset.csv')
        self.inflow_df = self.inflow_df[self.inflow_df['RESERVOIR'] == reservoir]
        inflow_df_1 = self.inflow_df[(self.inflow_df['MONTH'] < 6) & (self.inflow_df['YEAR'] == end_year)]
        inflow_df_2 = self.inflow_df[(self.inflow_df['MONTH'] >= 6) & (self.inflow_df['YEAR'] == start_year)]
        self.inflow_df = inflow_df_1.append(inflow_df_2, ignore_index=True)
        self.inflow_df['DD-MM-YYYY'] = self.inflow_df['DATE'].astype(str) + '-' + self.inflow_df['MONTH'].astype(str) + '-' + self.inflow_df['YEAR'].astype(str)
        self.__fill_missing_actual_inflow_outflow()
        self.inflow_df = self.inflow_df.sort_values(['YEAR', 'MONTH', 'DATE']).reset_index(drop=True)
        self.inflow_df['INTERVAL'] = self.__get_interval_column(self.inflow_df)
        self.inflow_df['SEASON'] = self.__get_season(self.inflow_df['MONTH'])

    def __load_all_actual_inflow_df(self, reservoir, start_year):
        try:
            if start_year > 2011:
                reservoir = reservoir.replace('.', '')
                self.all_actual_inflow_df = pd.read_csv(f'predictions/{reservoir}/all_actual_inflow.csv', index_col=0)
                self.all_actual_inflow_df = self.all_actual_inflow_df[self.all_actual_inflow_df.columns[self.all_actual_inflow_df.columns.str.split('-').str[0].astype(int) < start_year]]                
            else:
                self.all_actual_inflow_df = None
        except FileNotFoundError:
            self.all_actual_inflow_df = None
    
    def __load_all_amcs_outflow_df(self, reservoir, start_year):
        try:
            if start_year > 2011:
                reservoir = reservoir.replace('.', '')
                self.all_amcs_outflow_df = pd.read_csv(f'predictions/{reservoir}/all_amcs_outflow.csv', index_col=0)
                self.all_amcs_outflow_df = self.all_amcs_outflow_df[self.all_amcs_outflow_df.columns[self.all_amcs_outflow_df.columns.str.split('-').str[0].astype(int) < start_year]]                
            else:
                self.all_amcs_outflow_df = None
        except FileNotFoundError:
            self.all_amcs_outflow_df = None
    
    def __fill_missing_actual_inflow_outflow(self):
        date = []
        inflow_cusecs = []
        outflow_cusecs = []
        year = []
        month = []
        timestamp = []
        for ddmmyyyy, inflow, outflow in self.pred_df[['DD-MM-YYYY', 'INFLOW', 'OUTFLOW']].values:
            if ddmmyyyy not in self.inflow_df['DD-MM-YYYY'].unique():
                dd, mm, yyyy = ddmmyyyy.split('-')
                timestamp.append(ddmmyyyy)
                inflow_cusecs.append(inflow)
                outflow_cusecs.append(outflow)
                date.append(int(dd))
                month.append(int(mm))
                year.append(int(yyyy))
        
        self.inflow_df = self.inflow_df.append(pd.DataFrame({'DD-MM-YYYY': timestamp,
                                                             'INFLOW_CUSECS': inflow_cusecs,
                                                             'OUTFLOW_CUECS': outflow_cusecs,
                                                             'DATE': date,
                                                             'MONTH': month,
                                                             'YEAR': year}), ignore_index=True)

    def __get_interval_column(self, df):
        interval_col = []
        month_list = [6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5]
        for idx, row in df.iterrows():
            date = row['DATE']
            interval = month_list.index(row['MONTH']) * 4
            if date >= 1 and date <= 7:
                interval += 1
            elif date >= 8 and date <= 14:
                interval += 2
            elif date >= 15 and date <= 21:
                interval += 3
            else:
                interval += 4

            interval_col.append(interval)
        return interval_col

    def __get_season(self, month_col):
        season_col = []
        season_month = {'WINTER': [1, 2],
                        'SUMMER': [3, 4, 5],
                        'MONSOON': [6, 7, 8, 9],
                        'POST-MONSOON': [10, 11, 12]
                       }
        
        for month in month_col.values:
            if month in season_month['WINTER']:
                season_col.append('WINTER')
            elif month in season_month['SUMMER']:
                season_col.append('SUMMER')
            elif month in season_month['MONSOON']:
                season_col.append('MONSOON')
            elif month in season_month['POST-MONSOON']:
                season_col.append('POST-MONSOON')
            else:
                raise Exception(f'Unknown month {month} in datestamp {ddmmyyyy}')
        
        return season_col
    
    def __get_outflow_plan(self, storage):
        expected_remaining_total_monsoon_inflow = self.pred_df[self.inflow_df['SEASON'].isin(['MONSOON', 'POST-MONSOON'])]['INFLOW'].sum()
        expected_remaining_total_non_monsoon_inflow = self.pred_df[self.inflow_df['SEASON'].isin(['WINTER', 'SUMMER'])]['INFLOW'].sum()
        expected_remaining_total_monsoon_tmc = 8.64e-05 * expected_remaining_total_monsoon_inflow
        expected_remaining_total_non_monsoon_tmc = 8.64e-05 * expected_remaining_total_non_monsoon_inflow
        
        remaining_monsoon_df = self.pred_df[self.pred_df['SEASON'].isin(['MONSOON', 'POST-MONSOON'])]
        remaining_non_monsoon_df = self.pred_df[self.pred_df['SEASON'].isin(['WINTER', 'SUMMER'])]
        outflow_monsoon_dist = remaining_monsoon_df['OUTFLOW'].values / (remaining_monsoon_df['OUTFLOW'].sum() if remaining_monsoon_df['OUTFLOW'].sum() > 0 else 1)
        outflow_non_monsoon_dist = remaining_non_monsoon_df['OUTFLOW'].values / (remaining_non_monsoon_df['OUTFLOW'].sum() if remaining_non_monsoon_df['OUTFLOW'].sum() > 0 else 1)

        water_to_dispatch_monsoon_tmc = expected_remaining_total_monsoon_tmc + storage - self.total_capacity * 1.5
        water_to_dispatch_non_monsoon_tmc = expected_remaining_total_non_monsoon_tmc + self.total_capacity * 1.2
        new_outflow_list = np.append((outflow_monsoon_dist * water_to_dispatch_monsoon_tmc * 11574.074), (outflow_non_monsoon_dist * water_to_dispatch_non_monsoon_tmc * 11574.074))
    
    def __get_outflow(self, interval, storage, season):

        pred_remaining_df = self.pred_df[self.pred_df['INTERVAL'] > interval]
        pred_remaining_start_idx = pred_remaining_df.index[0]
        remaining_old_pred_outflow = pred_remaining_df['OUTFLOW'].values
#         remaining_old_pred_outflow[remaining_old_pred_outflow == 0] = 1

        # we calculate distribution of remaining weeks
        remaining_season_outflow_sum = pred_remaining_df.groupby('SEASON')['OUTFLOW'].apply(sum)
        remaining_season_monsoon_outflow_sum = 0
        remaining_season_monsoon_outflow_sum += remaining_season_outflow_sum['MONSOON'] if 'MONSOON' in remaining_season_outflow_sum.index else 0
        remaining_season_monsoon_outflow_sum += remaining_season_outflow_sum['POST-MONSOON'] if 'POST-MONSOON' in remaining_season_outflow_sum.index else 0
        remaining_season_non_monsoon_outflow_sum = 0
        remaining_season_non_monsoon_outflow_sum += remaining_season_outflow_sum['WINTER'] if 'WINTER' in remaining_season_outflow_sum.index else 0
        remaining_season_non_monsoon_outflow_sum += remaining_season_outflow_sum['SUMMER'] if 'SUMMER' in remaining_season_outflow_sum.index else 0
        
        expected_remaining_total_monsoon_inflow = self.pred_df[(self.pred_df['INTERVAL'] > interval) & (self.inflow_df['SEASON'].isin(['MONSOON', 'POST-MONSOON']))]['INFLOW'].sum()
        expected_remaining_total_non_monsoon_inflow = self.pred_df[(self.pred_df['INTERVAL'] > interval) & (self.inflow_df['SEASON'].isin(['WINTER', 'SUMMER']))]['INFLOW'].sum()
        expected_remaining_total_monsoon_tmc = 8.64e-05 * expected_remaining_total_monsoon_inflow
        expected_remaining_total_non_monsoon_tmc = 8.64e-05 * expected_remaining_total_non_monsoon_inflow

        num_days_in_interval = self.pred_df[self.pred_df['INTERVAL'] == interval - 1].shape[0]
        actual_inflow = self.inflow_df[self.inflow_df['INTERVAL'] == interval - 1]['INFLOW_CUSECS'].sum()
        pred_inflow = self.pred_df[self.pred_df['INTERVAL'] == interval - 1]['INFLOW'].sum()

        inflow_deviation = actual_inflow - pred_inflow
        deviation_tmc = 8.64e-05 * inflow_deviation * num_days_in_interval

        if self.drought:
            if self.drought == 'Slight':
                monsoon_end_storage_threshold = self.total_capacity * 0.9
                year_end_threshold = self.total_capacity * 0.15
            elif self.drought == 'Moderate':
                monsoon_end_storage_threshold = self.total_capacity * 0.7
                year_end_threshold = self.total_capacity * 0.05
            elif self.drought == 'Severe':
                monsoon_end_storage_threshold = self.total_capacity * 0.5
                year_end_threshold = 0
            
            if season in ['MONSOON', 'POST-MONSOON']:
                remaining_monsoon_count = pred_remaining_df[pred_remaining_df['SEASON'].isin(['MONSOON', 'POST-MONSOON'])].shape[0]
                remaining_non_monsoon_count = pred_remaining_df[pred_remaining_df['SEASON'].isin(['WINTER', 'SUMMER'])].shape[0]

#                 outflow_monsoon_dist = np.array([1]*(remaining_monsoon_count)) / (remaining_monsoon_count)
#                 outflow_non_monsoon_dist = np.array([1]*(remaining_non_monsoon_count)) / (remaining_non_monsoon_count)

                remaining_monsoon_df = pred_remaining_df[pred_remaining_df['SEASON'].isin(['MONSOON', 'POST-MONSOON'])]
                remaining_non_monsoon_df = pred_remaining_df[pred_remaining_df['SEASON'].isin(['WINTER', 'SUMMER'])]
                outflow_monsoon_dist = remaining_monsoon_df['OUTFLOW'].values / (remaining_monsoon_df['OUTFLOW'].sum() if remaining_monsoon_df['OUTFLOW'].sum() > 0 else 1)
                outflow_non_monsoon_dist = remaining_non_monsoon_df['OUTFLOW'].values / (remaining_non_monsoon_df['OUTFLOW'].sum() if remaining_non_monsoon_df['OUTFLOW'].sum() > 0 else 1)
                
                water_to_dispatch_monsoon_tmc = expected_remaining_total_monsoon_tmc + storage - monsoon_end_storage_threshold
                water_to_dispatch_non_monsoon_tmc = expected_remaining_total_non_monsoon_tmc + monsoon_end_storage_threshold - year_end_threshold


                new_outflow_list = np.append((outflow_monsoon_dist * water_to_dispatch_monsoon_tmc * 11574.074), (outflow_non_monsoon_dist * water_to_dispatch_non_monsoon_tmc * 11574.074))
                print('a')
            elif season in ['WINTER', 'SUMMER']:
                water_to_dispatch_tmc = expected_remaining_total_non_monsoon_tmc + storage - year_end_threshold
                print(water_to_dispatch_tmc)
                print(remaining_old_pred_outflow)
                outflow_dist = remaining_old_pred_outflow / (remaining_old_pred_outflow.sum() if remaining_old_pred_outflow.sum() > 0 else 1)#remaining_outflow_dist / remaining_outflow_dist.sum()
                new_outflow_list = outflow_dist * water_to_dispatch_tmc * 11574.074
                print('b')
        else:
            if deviation_tmc > 0:
                remaining_outflow_cross_dist = []
                for season in pred_remaining_df['SEASON'].values:
                    if season in ['MONSOON', 'POST-MONSOON']:
                        remaining_outflow_cross_dist.append(remaining_season_non_monsoon_outflow_sum)
                    elif remaining_season_monsoon_outflow_sum > 0:
                        remaining_outflow_cross_dist.append(remaining_season_monsoon_outflow_sum)
                    elif remaining_season_monsoon_outflow_sum == 0:
                        remaining_outflow_cross_dist.append(1)
                print(remaining_outflow_cross_dist)
                remaining_outflow_cross_dist = np.array(remaining_outflow_cross_dist) / sum(remaining_outflow_cross_dist)
#                 print(remaining_outflow_cross_dist)
                
                outflow_dist = remaining_outflow_cross_dist.copy()
                print('c')
            else:
                remaining_outflow_dist = []
                for season in pred_remaining_df['SEASON'].values:
                    if season in ['MONSOON', 'POST-MONSOON']:
                        remaining_outflow_dist.append(remaining_season_monsoon_outflow_sum)
                    elif remaining_season_monsoon_outflow_sum > 0:
                        remaining_outflow_dist.append(remaining_season_non_monsoon_outflow_sum)
                    elif remaining_season_monsoon_outflow_sum == 0:
                        remaining_outflow_dist.append(1)
                        
                remaining_outflow_dist = np.array(remaining_outflow_dist) / sum(remaining_outflow_dist)
                
                outflow_dist = remaining_outflow_dist.copy()
                print('d')
            
            new_outflow_list = remaining_old_pred_outflow + outflow_dist * deviation_tmc * 11574.074

#                 abs_deviation = np.abs(np.array(self.deviation[pred_remaining_start_idx:]))
#                 abs_deviation_sum = abs_deviation.sum()
#                 if max(self.deviation[pred_remaining_start_idx:]) > 0 and (max(abs_deviation) / abs_deviation_sum) * abs(deviation_tmc) * 11574.074 < max(abs_deviation):

#                     inflow_dist_normal = abs_deviation / abs_deviation.sum()
#                     # pd.DataFrame({'dev_inflow_dist_normal': inflow_dist_normal, 'outflow_dist': inflow_dist_normal * deviation_tmc * 11574.074}).to_csv('Examine.csv')
#                 else:
#                     inflow_dist_normal = remaining_inflow_values / remaining_inflow_values.sum()

            
#             plt.plot(self.model_predicted_outflow, label='OLD')
#             plt.plot(self.pred_df['OUTFLOW'], label='NEW')
#             plt.legend()
#             plt.show(block=True)
#         plt.plot(new_outflow_list)
#         plt.show(block=True)
#         new_outflow_list = np.minimum(new_outflow_list, (remaining_old_pred_outflow * 2))
        new_outflow_list[new_outflow_list < 0] = 0
#             np.minimum(outflow, self.model_predicted_outflow * 1.5) if self.model_predicted_outflow[idx] > 0 else outflow
        self.pred_df.loc[pred_remaining_start_idx:, ('OUTFLOW')] = new_outflow_list
#         self.deviation[pred_remaining_start_idx:] = new_outflow_list - self.model_predicted_outflow[pred_remaining_start_idx:]
        if self.pred_df[self.pred_df.isnull().any(axis=1)].shape[0] > 0:
            print(self.pred_df[self.pred_df.isnull().any(axis=1)])
            raise Exception()

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
                self.drought = False
        else:
            self.drought = False
    
    def __get_storage(self, inflow, outflow, storage, idx):
#         outflow = min(outflow, self.model_predicted_outflow[idx] * 2)
        inflow_tmc = 8.64e-05 * inflow
        outflow_tmc = 8.64e-05 * outflow
        print(outflow, outflow_tmc)
        storage = storage + inflow_tmc
        if outflow_tmc > storage or storage == 0:
            outflow = 11574.074 * storage
            storage = 0
        else:
            storage -= outflow_tmc
        
        if storage > self.total_capacity:
            outflow += 11574.074 * (storage - self.total_capacity)
            storage = self.total_capacity
        
        
        storage_pct = storage * 100 / self.total_capacity
        
        return int(outflow), round(storage, 2), round(storage_pct, 1)
    
    def __get_reservoir_duration(self, storage, idx):
        ndays = 0
        date = 1
        month = 6
        while storage > 0:
            ndays += 1
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
    
    def run(self, storage):
        amcs_outflow = {}
        self.pred_df.merge(self.inflow_df, on='DD-MM-YYYY')
        amcs_outflow['ACTUAL INFLOW'] = self.inflow_df[['DD-MM-YYYY', 'INFLOW_CUSECS']].set_index('DD-MM-YYYY')['INFLOW_CUSECS'].to_dict()
        amcs_outflow['ACTUAL OUTFLOW'] = self.inflow_df[['DD-MM-YYYY', 'OUTFLOW_CUECS']].set_index('DD-MM-YYYY')['OUTFLOW_CUECS'].to_dict()
        amcs_outflow['AMCS OUTFLOW'] = {}
        amcs_outflow['AMCS STORAGE'] = {}
        amcs_outflow['AMCS STORAGE PCT'] = {}
        amcs_outflow['NORMAL INFLOW'] = {}
        amcs_outflow['NORMAL OUTFLOW'] = {}
        amcs_outflow['DURATION'] = {}
        prev_interval = None
        cum_actual_inflow = 0
        cum_normal_inflow = 0
        for idx, row in self.pred_df.iterrows():
            interval = row['INTERVAL']
            season = row['SEASON']
            outflow = float(self.pred_df.loc[idx, ('OUTFLOW')])
            ddmmyyyy = row['DD-MM-YYYY']
            ddmm = '-'.join(ddmmyyyy.split('-')[:-1])
            actual_inflow = amcs_outflow['ACTUAL INFLOW'][ddmmyyyy]
            normal_inflow = self.all_actual_inflow_df.loc[ddmm].mean() if self.all_actual_inflow_df is not None else 0
            normal_outflow = self.all_amcs_outflow_df.loc[ddmm].mean() if self.all_amcs_outflow_df is not None else 0
            
            cum_actual_inflow += actual_inflow
            cum_normal_inflow += normal_inflow
            self.__drought_prediction(cum_actual_inflow, cum_normal_inflow)
                            
            if ddmm == '1-6':
                self.__get_outflow_plan(storage)
            
            if interval > 1 and prev_interval != interval and interval < 48:
                self.__get_outflow(interval, storage, season)
                prev_interval = interval
                print()
            
#                 if idx > 225:
# #     #               
#                 plt.plot(self.model_predicted_outflow, label='OLD')
#                 plt.plot(self.pred_df['OUTFLOW'], label='NEW')
#                 plt.title(f'{ddmmyyyy}-{storage}')
#                 plt.legend()
#                 plt.show(block=True)
            
            print(ddmmyyyy)
            
            print(outflow)
            
            outflow, storage, storage_pct = self.__get_storage(actual_inflow, outflow, storage, idx)
            duration = self.__get_reservoir_duration(storage, idx)
            amcs_outflow['AMCS OUTFLOW'][ddmmyyyy] = outflow
            amcs_outflow['AMCS STORAGE'][ddmmyyyy] = storage
            amcs_outflow['AMCS STORAGE PCT'][ddmmyyyy] = storage_pct
            amcs_outflow['NORMAL INFLOW'][ddmmyyyy] = normal_inflow
            amcs_outflow['NORMAL OUTFLOW'][ddmmyyyy] = normal_outflow
            amcs_outflow['DURATION'][ddmmyyyy] = duration

        return amcs_outflow