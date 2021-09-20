from xgboost import XGBRegressor

class XGBoostModel:
    def __init__(self, filename):
        self.model = XGBRegressor()
        self.model.load_model(filename)
    
    def __call__(self, x):
        return self.model.predict(x)
