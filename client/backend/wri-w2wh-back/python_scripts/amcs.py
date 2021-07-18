import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class AMCS:
    def __init__(self, model_prediction, reservoir, start_year, end_year):
        self.__get_pred_df(model_prediction)
        self.__load_inflow_df(reservoir, start_year, end_year)

        self.deviation = [0] * self.pred_df.shape[0]
        self.normal_outflow = self.pred_df['OUTFLOW'].tolist()
    
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
        self.__fill_missing_actual_inflow()
        self.inflow_df = self.inflow_df.sort_values(['YEAR', 'MONTH', 'DATE']).reset_index(drop=True)
        self.inflow_df['INTERVAL'] = self.__get_interval_column(self.inflow_df)

    def __fill_missing_actual_inflow(self):
        date = []
        inflow_cusecs = []
        year = []
        month = []
        timestamp = []
        for ddmmyyyy, inflow in self.pred_df[['DD-MM-YYYY', 'INFLOW']].values:
            if ddmmyyyy not in self.inflow_df['DD-MM-YYYY'].unique():
                dd, mm, yyyy = ddmmyyyy.split('-')
                timestamp.append(ddmmyyyy)
                inflow_cusecs.append(inflow)
                date.append(int(dd))
                month.append(int(mm))
                year.append(int(yyyy))
        
        self.inflow_df = self.inflow_df.append(pd.DataFrame({'DD-MM-YYYY': timestamp,
                                                             'INFLOW_CUSECS': inflow_cusecs,
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

    def __get_outflow(self, interval, drought=False):

        pred_remaining_df = self.pred_df[self.pred_df['INTERVAL'] > interval]
        pred_remaining_start_idx = pred_remaining_df.index[0]
        remaining_old_pred_outflow = pred_remaining_df['OUTFLOW'].values

        # we calculate distribution of remaining weeks
        remaining_inflow_values = pred_remaining_df['OUTFLOW'].values
        remaining_inflow_values[remaining_inflow_values == 0] = 1

        num_days_in_interval = self.pred_df[self.pred_df['INTERVAL'] == interval].shape[0]
        actual_inflow = self.inflow_df[self.inflow_df['INTERVAL'] == interval]['INFLOW_CUSECS'].sum()
        pred_inflow = self.pred_df[self.pred_df['INTERVAL'] == interval]['INFLOW'].sum()

        inflow_deviation = pred_inflow - actual_inflow
        deviation_tmc = 8.64e-05 * inflow_deviation * num_days_in_interval
        if inflow_deviation != 0:
            if drought:
                inflow_dist_normal = np.array([1]*(pred_remaining_df.shape[0])) / (pred_remaining_df.shape[0])
                deviation_tmc = deviation_tmc * 0.4
            else:

                if inflow_deviation > 0:
                    deviation_tmc = deviation_tmc * 0.7
                    rev_inflow_dist = 1 / remaining_inflow_values
                    inflow_dist_normal = rev_inflow_dist / rev_inflow_dist.sum()
                    row = {'rev': rev_inflow_dist, 'dist_normal': inflow_dist_normal, 'final': inflow_dist_normal * deviation_tmc * 11574.074, 'outflow': inflow_dist_normal * deviation_tmc * 11574.074 + remaining_old_pred_outflow}
                    pd.DataFrame(row).to_csv('Examine.csv')

                else:
                    deviation_tmc = deviation_tmc * 0.7
                    abs_deviation = np.abs(np.array(self.deviation[pred_remaining_start_idx:]))
                    abs_deviation_sum = abs_deviation.sum()
                    if max(self.deviation[pred_remaining_start_idx:]) > 0 and (max(abs_deviation) / abs_deviation_sum) * abs(deviation_tmc) * 11574.074 < max(abs_deviation):

                        inflow_dist_normal = abs_deviation / abs_deviation.sum()
                        pd.DataFrame({'dev_inflow_dist_normal': inflow_dist_normal, 'outflow_dist': inflow_dist_normal * deviation_tmc * 11574.074}).to_csv('Examine.csv')
                    else:
                        inflow_dist_normal = remaining_inflow_values / remaining_inflow_values.sum()
            new_outflow_list = inflow_dist_normal * deviation_tmc * 11574.074 + remaining_old_pred_outflow
            assert np.abs((inflow_dist_normal * np.abs(deviation_tmc)).sum() - np.abs(deviation_tmc)) < 0.1
            new_outflow_list[new_outflow_list < 0] = 0
            self.pred_df.loc[pred_remaining_start_idx:, ('OUTFLOW')] = new_outflow_list
            self.deviation[pred_remaining_start_idx:] = new_outflow_list - self.normal_outflow[pred_remaining_start_idx:]

    def __get_storage(self, inflow, outflow, storage):
        inflow_tmc = 8.64e-05 * inflow
        outflow_tmc = 8.64e-05 * outflow
        storage = storage + inflow_tmc
        if outflow_tmc > storage or storage == 0:
            outflow = 11574.074 * storage
            storage = 0
        else:
            storage -= outflow_tmc
        
        return outflow, storage
    
    def run(self, storage):
        amcs_outflow = {}
        self.pred_df.merge(self.inflow_df, on='DD-MM-YYYY')
        amcs_outflow['ACTUAL INFLOW'] = self.inflow_df[['DD-MM-YYYY', 'INFLOW_CUSECS']].set_index('DD-MM-YYYY')['INFLOW_CUSECS'].to_dict()
        amcs_outflow['AMCS OUTFLOW'] = {}
        amcs_outflow['AMCS STORAGE'] = {}
#         amcs_outflow['AMCS OUTFLOW'] = self.pred_df[['DD-MM-YYYY', 'OUTFLOW']].set_index('DD-MM-YYYY')['OUTFLOW'].to_dict()
        prev_interval = None
        for idx, row in self.pred_df.iterrows():
            interval = row['INTERVAL']
            outflow = self.pred_df.loc[idx, ('OUTFLOW')]
            ddmmyyyy = row['DD-MM-YYYY']
            actual_inflow = amcs_outflow['ACTUAL INFLOW'][ddmmyyyy]
            
            if interval > 1 and prev_interval != interval and interval < 48:
                self.__get_outflow(interval)
            
            
            outflow, storage = self.__get_storage(actual_inflow, outflow, storage)
            amcs_outflow['AMCS OUTFLOW'][ddmmyyyy] = outflow
            amcs_outflow['AMCS STORAGE'][ddmmyyyy] = storage
            
            
            
            
#         for interval in range(48):
#             self.__get_outflow(interval)
#             amcs_outflow[interval] = self.pred_df[['DD-MM-YYYY', 'OUTFLOW']].set_index('DD-MM-YYYY')['OUTFLOW'].to_dict()
        return amcs_outflow