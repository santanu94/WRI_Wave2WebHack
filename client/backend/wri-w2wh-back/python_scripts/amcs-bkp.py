import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

class AMCS:
    def __init__(self, model_prediction, reservoir, total_capacity, start_year, end_year):
        self.start_year = start_year
        self.total_capacity = total_capacity
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

    def __get_season(self, ddmmyyyy):
        season_month = {'WINTER': ['1', '2'],
                        'SUMMER': ['3', '4', '5'],
                        'MONSOON': ['6', '7', '8', '9'],
                        'POST-MONSOON': ['10', '11', '12']
                       }
        month = ddmmyyyy.split('-')[1]
        if month in season_month['WINTER']:
            return 'WINTER'
        elif month in season_month['SUMMER']:
            return 'SUMMER'
        elif month in season_month['MONSOON']:
            return 'MONSOON'
        elif month in season_month['POST-MONSOON']:
            return 'POST-MONSOON'
        else:
            raise Exception(f'Unknown month {month} in datestamp {ddmmyyyy}')
    
#     def __get_outflow(self, interval, storage_pct, season, drought):

#         pred_remaining_df = self.pred_df[self.pred_df['INTERVAL'] > interval]
#         pred_remaining_start_idx = pred_remaining_df.index[0]
#         remaining_old_pred_outflow = pred_remaining_df['OUTFLOW'].values

#         # we calculate distribution of remaining weeks
#         remaining_inflow_values = pred_remaining_df['OUTFLOW'].values
#         remaining_inflow_values[remaining_inflow_values == 0] = 1

#         num_days_in_interval = self.pred_df[self.pred_df['INTERVAL'] == interval].shape[0]
#         actual_inflow = self.inflow_df[self.inflow_df['INTERVAL'] == interval]['INFLOW_CUSECS'].sum()
#         pred_inflow = self.pred_df[self.pred_df['INTERVAL'] == interval]['INFLOW'].sum()

#         inflow_deviation = actual_inflow - pred_inflow
#         deviation_tmc = 8.64e-05 * inflow_deviation * num_days_in_interval
#         print('Actual inflw -', actual_inflow, 'pred inflow -', pred_inflow)
# #         if inflow_deviation != 0:
#         print(inflow_deviation)
#         if drought:
#             if drought == 'Slight':
#                 inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
#                 deviation_tmc = abs(deviation_tmc) * 0.1
#             elif drought == 'Moderate':
#                 inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
#                 deviation_tmc = abs(deviation_tmc) * 0.2
#             elif drought == 'Severe':
#                 inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
#                 deviation_tmc = abs(deviation_tmc) * 0.3
# #                 inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
# #                 deviation_tmc = deviation_tmc * 0.4
#         else:
#             if season in ['WINTER', 'SUMMER']:
#                 if storage_pct > 50:
#             elif if season in ['MONSOON', 'POST-MONSOON']:
#             else:
#                 raise Exception('Unknown season')

#             if inflow_deviation > 0:
# #                 if season in ['WINTER', 'SUMMER']:
#                 if storage_pct >= 85:
#                     print('a')
#                     deviation_tmc = deviation_tmc * 2
#                 elif storage_pct <= 40:
#                     print('b')
#                     deviation_tmc = deviation_tmc * 1
# #                     elif storage_pct > 90:
# #                         deviation_tmc = deviation_tmc * 0.99
# #                     else:
# #                         deviation_tmc = deviation_tmc * 0.8
# #                     deviation_tmc = deviation_tmc * 1
#                 rev_inflow_dist = 1 / remaining_inflow_values
#                 inflow_dist_normal = rev_inflow_dist / rev_inflow_dist.sum()
#                 # row = {'rev': rev_inflow_dist, 'dist_normal': inflow_dist_normal, 'final': inflow_dist_normal * deviation_tmc * 11574.074, 'outflow': inflow_dist_normal * deviation_tmc * 11574.074 + remaining_old_pred_outflow}
#                 # pd.DataFrame(row).to_csv('Examine.csv')

#             else:
#                 if season in ['WINTER', 'SUMMER']:
#                     if storage_pct >= 85:
#                         print('c')
#                         deviation_tmc = deviation_tmc * -1
#                     elif storage_pct <= 40:
#                         print('d')
#                         deviation_tmc = deviation_tmc * 0
# #                     if storage_pct <= 50:
# #                         deviation_tmc = deviation_tmc * 1
# #                     elif storage_pct > 90:
# #                         deviation_tmc = deviation_tmc * 0.1
# #                     else:
# #                         deviation_tmc = deviation_tmc * 0.4
# #                     deviation_tmc = deviation_tmc * -10#0.05
#                 abs_deviation = np.abs(np.array(self.deviation[pred_remaining_start_idx:]))
#                 abs_deviation_sum = abs_deviation.sum()
#                 if max(self.deviation[pred_remaining_start_idx:]) > 0 and (max(abs_deviation) / abs_deviation_sum) * abs(deviation_tmc) * 11574.074 < max(abs_deviation):

#                     inflow_dist_normal = abs_deviation / abs_deviation.sum()
#                     # pd.DataFrame({'dev_inflow_dist_normal': inflow_dist_normal, 'outflow_dist': inflow_dist_normal * deviation_tmc * 11574.074}).to_csv('Examine.csv')
#                 else:
#                     inflow_dist_normal = remaining_inflow_values / remaining_inflow_values.sum()

#         new_outflow_list = inflow_dist_normal * deviation_tmc * 11574.074 + remaining_old_pred_outflow
#         assert np.abs((inflow_dist_normal * np.abs(deviation_tmc)).sum() - np.abs(deviation_tmc)) < 0.1
# #             plt.plot(remaining_old_pred_outflow, label='OLD')
# #             plt.plot(new_outflow_list, label='NEW')
# #             plt.legend()
# #             plt.show(block=True)
#         new_outflow_list = np.minimum(new_outflow_list, (remaining_old_pred_outflow * 3))
#         new_outflow_list[new_outflow_list < 0] = 0
# #             min(outflow, self.model_predicted_outflow[idx] * 1.5) if self.model_predicted_outflow[idx] > 0 else outflow
#         self.pred_df.loc[pred_remaining_start_idx:, ('OUTFLOW')] = new_outflow_list
#         self.deviation[pred_remaining_start_idx:] = new_outflow_list - self.model_predicted_outflow[pred_remaining_start_idx:]

        def __get_outflow(self, interval, storage_pct, season, drought):

        pred_remaining_df = self.pred_df[self.pred_df['INTERVAL'] > interval]
        pred_remaining_start_idx = pred_remaining_df.index[0]
        remaining_old_pred_outflow = pred_remaining_df['OUTFLOW'].values

        # we calculate distribution of remaining weeks
        remaining_inflow_values = pred_remaining_df['OUTFLOW'].values
        remaining_inflow_values[remaining_inflow_values == 0] = 1

        num_days_in_interval = self.pred_df[self.pred_df['INTERVAL'] == interval].shape[0]
        actual_inflow = self.inflow_df[self.inflow_df['INTERVAL'] == interval]['INFLOW_CUSECS'].sum()
        pred_inflow = self.pred_df[self.pred_df['INTERVAL'] == interval]['INFLOW'].sum()

        inflow_deviation = actual_inflow - pred_inflow
        deviation_tmc = 8.64e-05 * inflow_deviation * num_days_in_interval
        print('Actual inflw -', actual_inflow, 'pred inflow -', pred_inflow)
#         if inflow_deviation != 0:
        print(inflow_deviation)
        if drought:
            if drought == 'Slight':
                inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
                deviation_tmc = abs(deviation_tmc) * 0.1
            elif drought == 'Moderate':
                inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
                deviation_tmc = abs(deviation_tmc) * 0.2
            elif drought == 'Severe':
                inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
                deviation_tmc = abs(deviation_tmc) * 0.3
#                 inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
#                 deviation_tmc = deviation_tmc * 0.4
        else:
            if season in ['WINTER', 'SUMMER']:
                storage_threshold = self.total_storage * 0.2
                water_to_dispatch_tmc = storage - storage_threshold
                outflow_dist = remaining_inflow_values / remaining_inflow_values.sum()
#                 else:
#                     water_to_dispatch_tmc = storage_threshold - storage
            elif if season in ['MONSOON', 'POST-MONSOON']:
                
            else:
                raise Exception('Unknown season')

            if inflow_deviation > 0:
#                 if season in ['WINTER', 'SUMMER']:
                if storage_pct >= 85:
                    print('a')
                    deviation_tmc = deviation_tmc * 2
                elif storage_pct <= 40:
                    print('b')
                    deviation_tmc = deviation_tmc * 1
#                     elif storage_pct > 90:
#                         deviation_tmc = deviation_tmc * 0.99
#                     else:
#                         deviation_tmc = deviation_tmc * 0.8
#                     deviation_tmc = deviation_tmc * 1
                rev_inflow_dist = 1 / remaining_inflow_values
                inflow_dist_normal = rev_inflow_dist / rev_inflow_dist.sum()
                # row = {'rev': rev_inflow_dist, 'dist_normal': inflow_dist_normal, 'final': inflow_dist_normal * deviation_tmc * 11574.074, 'outflow': inflow_dist_normal * deviation_tmc * 11574.074 + remaining_old_pred_outflow}
                # pd.DataFrame(row).to_csv('Examine.csv')

            else:
                if season in ['WINTER', 'SUMMER']:
                    if storage_pct >= 85:
                        print('c')
                        deviation_tmc = deviation_tmc * -1
                    elif storage_pct <= 40:
                        print('d')
                        deviation_tmc = deviation_tmc * 0
#                     if storage_pct <= 50:
#                         deviation_tmc = deviation_tmc * 1
#                     elif storage_pct > 90:
#                         deviation_tmc = deviation_tmc * 0.1
#                     else:
#                         deviation_tmc = deviation_tmc * 0.4
#                     deviation_tmc = deviation_tmc * -10#0.05
                abs_deviation = np.abs(np.array(self.deviation[pred_remaining_start_idx:]))
                abs_deviation_sum = abs_deviation.sum()
                if max(self.deviation[pred_remaining_start_idx:]) > 0 and (max(abs_deviation) / abs_deviation_sum) * abs(deviation_tmc) * 11574.074 < max(abs_deviation):

                    inflow_dist_normal = abs_deviation / abs_deviation.sum()
                    # pd.DataFrame({'dev_inflow_dist_normal': inflow_dist_normal, 'outflow_dist': inflow_dist_normal * deviation_tmc * 11574.074}).to_csv('Examine.csv')
                else:
                    inflow_dist_normal = remaining_inflow_values / remaining_inflow_values.sum()

        new_outflow_list = inflow_dist_normal * deviation_tmc * 11574.074 + remaining_old_pred_outflow
        assert np.abs((inflow_dist_normal * np.abs(deviation_tmc)).sum() - np.abs(deviation_tmc)) < 0.1
#             plt.plot(remaining_old_pred_outflow, label='OLD')
#             plt.plot(new_outflow_list, label='NEW')
#             plt.legend()
#             plt.show(block=True)
        new_outflow_list = np.minimum(new_outflow_list, (remaining_old_pred_outflow * 3))
        new_outflow_list[new_outflow_list < 0] = 0
#             min(outflow, self.model_predicted_outflow[idx] * 1.5) if self.model_predicted_outflow[idx] > 0 else outflow
        self.pred_df.loc[pred_remaining_start_idx:, ('OUTFLOW')] = new_outflow_list
        self.deviation[pred_remaining_start_idx:] = new_outflow_list - self.model_predicted_outflow[pred_remaining_start_idx:]

    def __drought_prediction(self, actual_inflow, normal_inflow):
        if actual_inflow < normal_inflow:
            inflow_deficiency = (normal_inflow - actual_inflow) * 100 / normal_inflow

            if inflow_deficiency > 10 and inflow_deficiency <= 25:
                return 'Slight'
            elif inflow_deficiency > 25 and inflow_deficiency <= 50:
                return 'Moderate'
            elif inflow_deficiency > 50:
                return 'Severe'
        else:
            return False
    
    def __get_storage(self, inflow, outflow, storage, idx):
        outflow = min(outflow, self.model_predicted_outflow[idx] * 1.5) if self.model_predicted_outflow[idx] > 0 else outflow
        inflow_tmc = 8.64e-05 * inflow
        outflow_tmc = 8.64e-05 * outflow
        storage = storage + inflow_tmc
        if outflow_tmc > storage or storage == 0:
            outflow = 11574.074 * storage
            storage = 0
        elif storage > self.total_capacity:
            outflow = 11574.074 * (storage - self.total_capacity)
            storage = self.total_capacity
        else:
            storage -= outflow_tmc
        
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
        for idx, row in self.pred_df.iterrows():
            interval = row['INTERVAL']
            outflow = float(self.pred_df.loc[idx, ('OUTFLOW')])
            ddmmyyyy = row['DD-MM-YYYY']
            ddmm = '-'.join(ddmmyyyy.split('-')[:-1])
            actual_inflow = amcs_outflow['ACTUAL INFLOW'][ddmmyyyy]
            normal_inflow = self.all_actual_inflow_df.loc[ddmm].mean() if self.all_actual_inflow_df is not None else 0
            normal_outflow = self.all_amcs_outflow_df.loc[ddmm].mean() if self.all_amcs_outflow_df is not None else 0
            drought = self.__drought_prediction(actual_inflow, normal_inflow)
                            
            
            if interval > 1 and prev_interval != interval and interval < 48:
                season = self.__get_season(ddmmyyyy)
                print(ddmmyyyy, season)
                self.__get_outflow(interval, storage_pct, season, drought)
                print()
                prev_interval = interval
            
            if ddmm.endswith('6'):
                print('yes')
                outflow = max(outflow, 2000)
            
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