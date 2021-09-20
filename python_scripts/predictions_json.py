from krs import KRS
from amcs import AMCS
from stats import Stats
import datetime
# import calendar
import json
from tqdm import tqdm
import argparse
import warnings
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Predict inflow for a year for a reservoir')
parser.add_argument('year', type=int, help='year to make predictins for')
args = parser.parse_args()

def cycle_loop(start_year):
    krs_obj = KRS(max_storage=49.45, curr_storage=curr_storage['KRS'], year=start_year)
    krs_amcs = AMCS(krs_obj, start_year)
    # global krs_obj, krs_amcs
    prediction = {}
    prediction['KRS'] = {}
    prediction['KRS']['INFLOW'] = {}
    prediction['KRS']['AMCS OUTFLOW'] = {}
    prediction['KRS']['AMCS STORAGE'] = {}
    prediction['KRS']['ACTUAL INFLOW'] = {}
    prediction['KRS']['ACTUAL OUTFLOW'] = {}
    stats_dict = {}
    stats_dict['KRS'] = {}

    loop_date = datetime.date(start_year, 6, 1)
    end_date = datetime.date(start_year+1, 6, 1)
    # end_date = datetime.date(start_year, 9, 1)
    delta = datetime.timedelta(days=1)
    pbar = tqdm(total=int(str(end_date-loop_date).split()[0]), initial=1)
    while loop_date < end_date:
        if loop_date.day in [8, 15, 22, 1]:
            krs_amcs.run(loop_date)
        
        krs_obj.predict_and_forecast(loop_date)
        # prediction['KRS']['INFLOW'].update(krs_prediction_dict['INFLOW'])
        # prediction['KRS']['AMCS OUTFLOW'].update(krs_prediction_dict['AMCS OUTFLOW'])
        # prediction['KRS']['AMCS STORAGE'].update(krs_prediction_dict['AMCS STORAGE'])
        # prediction['KRS']['ACTUAL INFLOW'].update(krs_prediction_dict['ACTUAL INFLOW'])
        # prediction['KRS']['ACTUAL OUTFLOW'].update(krs_prediction_dict['ACTUAL OUTFLOW'])
        
        # print(prediction)
        # import matplotlib.pyplot as plt
        # a = pd.DataFrame(prediction['KRS'])
        # a['INFLOW'].plot()
        # a['ACTUAL INFLOW'].plot()
        # plt.show()
        
        loop_date += delta
        pbar.update(1)
    
    krs_obj.trim_df_top()
    stats_dict['KRS'] = Stats(krs_obj.prediction_df.copy()).get_stats_dict(start_year=year, end_year=year+1)

    # Save prediction file
    prediction['KRS'] = krs_obj.prediction_df.set_index('date').to_dict()
    with open(f'predictions/KRS/predictions_{start_year}_{start_year+1}.json', "w") as f:
        json.dump(prediction['KRS'], f)
    
    with open(f'predictions/KRS/stats_{year}_{year+1}.json', "w") as f:
        json.dump(stats_dict['KRS'], f)
    
if __name__ == '__main__':
    year = args.year
    curr_storage = {}

    # 46.42
    if year == 2011:
        curr_storage['KRS'] = 17.13
    # if year == 2012:
    #     curr_storage['KRS'] = 8.45
    elif year > 2011:
        with open(f'predictions/KRS/stats_{year-1}_{year}.json') as f:
            prev_cycle_stats = json.load(f)
        curr_storage['KRS'] = prev_cycle_stats['FINAL STORAGE']
        
    cycle_loop(year)
