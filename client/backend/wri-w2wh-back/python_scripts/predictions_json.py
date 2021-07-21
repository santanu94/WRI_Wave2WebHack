from krs import KRS
from amcs import AMCS
from stats import Stats
import json
import argparse
import warnings
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Predict inflow for a year for a reservoir')
parser.add_argument('reservoir', type=str, help='can be one of ["KRS", "Kabini", "Hemavathi"]')
parser.add_argument('year', type=int, help='year to make predictins for')
args = parser.parse_args()

def save_predictions(reservoir, year, curr_storage):
    res_obj = None
    if reservoir == 'KRS':
        res_obj = KRS()
    else:
        print('Reservoir not found')
    
    # Get model predictions
    prediction = res_obj.get_predictions(curr_storage, year)
    
    if reservoir == 'KRS':
        reservoir_name = 'K.R.S'
    else:
        reservoir_name = reservoir
    
    # Get AMCS output
    amcs_out = AMCS(prediction.copy(), reservoir_name, year, year+1).run(curr_storage)
    prediction.update(amcs_out)
    
    # Get statistics from predictions
    stats_dict = Stats(prediction.copy(), reservoir).get_stats_dict(start_year=year, end_year=year+1)
    
    # Save prediction file
    with open(f'predictions/{reservoir}/predictions_{year}_{year+1}.json', "w") as f:
        json.dump(prediction, f)
    
    # Save stats file
    with open(f'predictions/{reservoir}/stats_{year}_{year+1}.json', "w") as f:
        json.dump(stats_dict, f)

if __name__ == '__main__':
    reservoir = args.reservoir
    year = args.year
    
    if reservoir not in ["KRS", "Kabini", "Hemavathi"]:
        print('Reservoir should be one of "KRS", "Kabini", "Hemavathi"')
    
    if year == 2011:
        curr_storage = 46.42
    else:
        with open(f'predictions/KRS/stats_{year-1}_{year}.json') as f:
            prev_cycle_stats = json.load(f)
        curr_storage = prev_cycle_stats['FINAL STORAGE']
    save_predictions(reservoir, year, curr_storage)