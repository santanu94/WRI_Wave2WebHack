import torch
import torch.nn as nn

class KRSInflowModel(nn.Module):
    def __init__(self, nmonth, nday, nseason):
        super().__init__()
        self.month_emb = nn.Embedding(num_embeddings=nmonth, embedding_dim=128)
        self.day_emb = nn.Embedding(num_embeddings=nday, embedding_dim=128)
        self.season_emb = nn.Embedding(num_embeddings=nseason, embedding_dim=128)
        self.prev_data_layer = nn.Sequential(
            nn.Linear(in_features=2, out_features=64),
            nn.ReLU(),
            nn.Linear(in_features=64, out_features=128),
            nn.ReLU()
        )
        self.hidden_layer = nn.Sequential(
            nn.Linear(in_features=128*4, out_features=768),
            nn.LeakyReLU(),
            nn.Linear(in_features=768, out_features=256),
            nn.LeakyReLU(),
        )
        self.rainfall_layer = nn.Sequential(
            nn.BatchNorm1d(num_features=256),
            nn.Linear(in_features=256, out_features=128),
            nn.LeakyReLU(),
            nn.Linear(in_features=128, out_features=64),
            nn.LeakyReLU(),
            nn.Linear(in_features=64, out_features=1),
            nn.ReLU()
        )
        
        self.inflow_layer = nn.Sequential(
            nn.BatchNorm1d(num_features=256),
            nn.Linear(in_features=256, out_features=64),
            nn.LeakyReLU(),
            nn.Linear(in_features=64, out_features=1),
            nn.ReLU()
        )
    
    def forward(self, x_month, x_day, x_season, x_prev_data):
        month_out = self.day_emb(x_month)
        day_out = self.day_emb(x_day)
        season_out = self.season_emb(x_season)
        prev_data_out = self.prev_data_layer(x_prev_data)

        x = torch.cat([month_out, day_out, season_out, prev_data_out], axis=1)
        hidden_out = self.hidden_layer(x)
        rainfall_out = self.rainfall_layer(hidden_out)
        inflow_out = self.inflow_layer(hidden_out)

        return rainfall_out, inflow_out
    
    def weight_init(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Embedding):
                nn.init.xavier_uniform_(m.weight)