import pandas as pd
import torch
from models import inflow_models as im
import pickle 
import json  
import argparse
import warnings
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Predict inflow for a year for a reservoir')
parser.add_argument('reservoir', type=str, help='can be one of ["KRS", "Kabini", "Hemavathi"]')
parser.add_argument('year', type=int, help='year to make predictins for')
args = parser.parse_args()

rainfall_departure_df = None
month_date_day_season_df = None
month_le = None
date_le = None
season_le = None
device = None
model = None


def init(reservoir):
    global rainfall_departure_df, month_date_day_season_df, month_le, date_le, season_le, device

    rainfall_departure_df = pd.read_csv('dataset/Rainfall 2010-2020/rainfall_departure_dataset.csv')
    if reservoir == 'KRS':
        rainfall_departure_df = rainfall_departure_df[rainfall_departure_df['DISTRICTS'] == 'KODAGU']
    else:
        raise Exception('Reservoir not found')
    rainfall_departure_df.drop(columns=['DISTRICTS'], inplace=True)

    with open('dataset/month_le.pkl', 'rb') as f:
        month_le = pickle.load(f)

    with open('dataset/date_le.pkl', 'rb') as f:
        date_le = pickle.load(f)

    with open('dataset/season_le.pkl', 'rb') as f:
        season_le = pickle.load(f)

    month_date_day_season_df = pd.read_csv('dataset/month_date_day_season.csv')
    month_date_day_season_df.sort_values(by=['MONTH', 'DATE'])
    
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

def load_model(reservoir):
    global model
    if reservoir == 'KRS':
        model = im.KRSInflowModel(len(month_le.classes_), len(date_le.classes_), len(season_le.classes_)).to(device)
        model.load_state_dict(torch.load('models/inflow_cnn_date.pth', map_location=device))
        model.eval()

def predict_inflow(month, date, season, year):
    prev_rainfall_departure_df = rainfall_departure_df[(rainfall_departure_df['YEAR'] < year) & (rainfall_departure_df['MONTH'] == month)].sort_values('YEAR', ascending=False).head(3)
    prev_avg_rainfall = prev_rainfall_departure_df['RAINFALL'].values.mean()
    prev_avg_departure = prev_rainfall_departure_df['DEPARTURE'].values.mean()

    month_transformed = month_le.transform([month])
    date_transformed = date_le.transform([date])
    season_transformed = season_le.transform([season])

    x_month = torch.tensor(month_transformed).to(device)
    x_date = torch.tensor(date_transformed).to(device)
    x_season = torch.tensor(season_transformed).to(device)
    x_prev_data = torch.FloatTensor([prev_avg_rainfall, prev_avg_departure]).view(1, -1).to(device)
    
    with torch.no_grad():
        y_hat = model(x_month, x_date, x_season, x_prev_data)
    
    return y_hat.view(1).cpu().item()

def get_prediction(reservoir, year):
    try:
        init(reservoir)
        load_model(reservoir)
        
        prediction = {}
        for idx, row in month_date_day_season_df.iterrows():
            month = row['MONTH']
            date = row['DATE']
            day = row['DAY']
            season = row['SEASON']

            inflow = predict_inflow(month, date, season, year)

            if year % 4 != 0 and month == 2 and date == 29:
                continue

            prediction[f'{date}-{month}-{year}'] = inflow
        
        with open(f'predictions/{reservoir}_inflow_{year}.json', "w") as f:
            json.dump(prediction, f)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    reservoir = args.reservoir
    year = args.year
    
    if reservoir not in ["KRS", "Kabini", "Hemavathi"]:
        print('Reservoir should be one of "KRS", "Kabini", "Hemavathi"')
    
    get_prediction(reservoir, year)
