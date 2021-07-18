import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class Stats:
    def __init__(self, predictions):
        self.pred_df = pd.DataFrame(predictions).reset_index()
        self.pred_df.rename(columns={'index': 'DD-MM-YYYY'}, inplace=True)
        self.pred_df['YEAR'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[2].astype(int)
        self.pred_df['MONTH'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[1].astype(int)
        self.pred_df['DATE'] = self.pred_df['DD-MM-YYYY'].str.split('-').str[0].astype(int)
        self.pred_df = self.pred_df.sort_values(['YEAR', 'MONTH', 'DATE']).reset_index(drop=True)
    
    def __get_annual_cumulative_inflow(self):
        return self.pred_df['ACTUAL INFLOW'].sum()
    
    def __get_monthly_cumulative_inflow(self):
        return self.pred_df.groupby('MONTH')['ACTUAL INFLOW'].apply(sum).to_dict()
    
    def get_stats_dict(self):
        stats_dict = {}
        
        stats_dict['MONTHLY CUMULATIVE'] = self.__get_monthly_cumulative_inflow()
        stats_dict['ANNUAL CUMULATIVE'] = self.__get_annual_cumulative_inflow()
        return stats_dict