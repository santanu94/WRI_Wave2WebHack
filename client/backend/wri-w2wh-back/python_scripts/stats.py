import pandas as pd
import numpy as np
import json
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
    
    def __get_daily_cumulative_inflow(self):
        return self.pred_df.set_index('DD-MM-YYYY')['ACTUAL INFLOW'].cumsum().to_dict()
    
    def __get_monthly_cumulative_inflow(self):
        return self.pred_df.groupby('MONTH')['ACTUAL INFLOW'].apply(sum).to_dict()
    
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
    
    def get_stats_dict(self, start_year, end_year):
        stats_dict = {}
        
        stats_dict['MONTHLY CUMULATIVE INFLOW'] = self.__get_monthly_cumulative_inflow()
        stats_dict['DAILY CUMULATIVE INFLOW'] = self.__get_daily_cumulative_inflow()
        stats_dict['FINAL STORAGE'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 5) & (self.pred_df['DATE'] == 31)]['AMCS STORAGE'].values[0]
        
        # AMCS impact on outflow in current cycle
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS'] = {}
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['WINTER'] = 0
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['SUMMER'] = 0
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['MONSOON'] = 0
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['POST-MONSOON'] = 0
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS'] = {}
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['WINTER'] = 0
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['SUMMER'] = 0
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['MONSOON'] = 0
        stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['POST-MONSOON'] = 0

        # AMCS impact on storage in current cycle
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE AMCS'] = {}
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE AMCS']['WINTER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 2) & (self.pred_df['DATE'] == 28 if end_year % 4 != 0 else 29)]['AMCS STORAGE'].values[0]
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE AMCS']['SUMMER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 5) & (self.pred_df['DATE'] == 31)]['AMCS STORAGE'].values[0]
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE AMCS']['MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 9) & (self.pred_df['DATE'] == 30)]['AMCS STORAGE'].values[0]
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE AMCS']['POST-MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 12) & (self.pred_df['DATE'] == 31)]['AMCS STORAGE'].values[0]
        
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE NO AMCS'] = {}
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE NO AMCS']['WINTER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 2) & (self.pred_df['DATE'] == 28 if end_year % 4 != 0 else 29)]['STORAGE'].values[0]
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE NO AMCS']['SUMMER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 5) & (self.pred_df['DATE'] == 31)]['STORAGE'].values[0]
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE NO AMCS']['MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 9) & (self.pred_df['DATE'] == 30)]['STORAGE'].values[0]
        stats_dict['CURRENT CYCLE FINAL SEASONAL STORAGE NO AMCS']['POST-MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 12) & (self.pred_df['DATE'] == 31)]['STORAGE'].values[0]
        
        prev_cycle_stats = None
        if start_year > 2011:
            with open(f'predictions/KRS/stats_{start_year-1}_{start_year}.json') as f:
                prev_cycle_stats = json.load(f)
            
            
            stats_dict['INFLOW CHANGE'] = {}
            for outflow, amcs_outflow, ddmmyyyy in self.pred_df[['OUTFLOW', 'AMCS OUTFLOW', 'DD-MM-YYYY']].values:
                
                # Change in Inflow compared to last year
                year = int(ddmmyyyy.split('-')[-1])
                prev_year = year - 1
                try:
                    stats_dict['INFLOW CHANGE'][ddmmyyyy] = round((stats_dict['DAILY CUMULATIVE INFLOW'][ddmmyyyy] - prev_cycle_stats['DAILY CUMULATIVE INFLOW'][ddmmyyyy[:-4]+str(prev_year)]) * 100 / prev_cycle_stats['DAILY CUMULATIVE INFLOW'][ddmmyyyy[:-4]+str(prev_year)], 1)
                except KeyError as e:
                    print('Error getting inflow change compared to last year current date')
                    print(e)
                
                stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS'][self.__get_season(ddmmyyyy)] += amcs_outflow
                stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS'][self.__get_season(ddmmyyyy)] += outflow
        else:
            for outflow, amcs_outflow, ddmmyyyy in self.pred_df[['OUTFLOW', 'AMCS OUTFLOW', 'DD-MM-YYYY']].values:
                stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS'][self.__get_season(ddmmyyyy)] += amcs_outflow
                stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS'][self.__get_season(ddmmyyyy)] += outflow
                    
        # AMCS impact on outflow (annual cumulative)
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS'] = {}
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['WINTER'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['WINTER']
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['SUMMER'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['SUMMER']
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['MONSOON'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['MONSOON']
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['POST-MONSOON'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW AMCS']['POST-MONSOON']
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS'] = {}
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['WINTER'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['WINTER']
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['SUMMER'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['SUMMER']
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['MONSOON'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['MONSOON']
        stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['POST-MONSOON'] = stats_dict['CURRENT CYCLE TOTAL SEASONAL OUTFLOW NO AMCS']['POST-MONSOON']

#         # AMCS impact on storage in (annual cumulative)
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE AMCS'] = {}
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE AMCS']['WINTER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 2) & (self.pred_df['DATE'] == 28 if end_year % 4 != 0 else 29)]['AMCS STORAGE']
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE AMCS']['SUMMER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 5) & (self.pred_df['DATE'] == 31)]['AMCS STORAGE']
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE AMCS']['MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 9) & (self.pred_df['DATE'] == 30)]['AMCS STORAGE']
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE AMCS']['POST-MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 12) & (self.pred_df['DATE'] == 31)]['AMCS STORAGE']
        
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE NO AMCS'] = {}
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE NO AMCS']['WINTER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 2) & (self.pred_df['DATE'] == 28 if end_year % 4 != 0 else 29)]['AMCS STORAGE']
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE NO AMCS']['SUMMER'] = self.pred_df[(self.pred_df['YEAR'] == end_year) & (self.pred_df['MONTH'] == 5) & (self.pred_df['DATE'] == 31)]['AMCS STORAGE']
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE NO AMCS']['MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 9) & (self.pred_df['DATE'] == 30)]['AMCS STORAGE']
#         stats_dict['ANNUAL CUMULATIVE FINAL SEASONAL STORAGE NO AMCS']['POST-MONSOON'] = self.pred_df[(self.pred_df['YEAR'] == start_year) & (self.pred_df['MONTH'] == 12) & (self.pred_df['DATE'] == 31)]['AMCS STORAGE']
        
        if prev_cycle_stats is not None:
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['WINTER'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['WINTER']
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['SUMMER'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['SUMMER']
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['MONSOON'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['MONSOON']
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['POST-MONSOON'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW AMCS']['POST-MONSOON']
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['WINTER'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['WINTER']
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['SUMMER'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['SUMMER']
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['MONSOON'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['MONSOON']
            stats_dict['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['POST-MONSOON'] += prev_cycle_stats['ANNUAL CUMULATIVE TOTAL SEASONAL OUTFLOW NO AMCS']['POST-MONSOON']





# (amcs_effect_df['OUTFLOW'] - amcs_effect_df['OLD_OUTFLOW']) * 100 / amcs_effect_df['OLD_OUTFLOW']
        return stats_dict