from krs import KRS
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
    
    prediction = res_obj.get_predictions(curr_storage, year)
    
    with open(f'predictions/{reservoir}_{year}_{year+1}.json', "w") as f:
        json.dump(prediction, f)

if __name__ == '__main__':
    reservoir = args.reservoir
    year = args.year
    
    if reservoir not in ["KRS", "Kabini", "Hemavathi"]:
        print('Reservoir should be one of "KRS", "Kabini", "Hemavathi"')
    
    curr_storage = 20
    save_predictions(reservoir, year, curr_storage)
