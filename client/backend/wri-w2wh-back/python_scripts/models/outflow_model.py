import torch
import torch.nn as nn

class OutflowModel(nn.Module):
    def __init__(self, nmonth, ndate, nseason):
        super().__init__()
        self.month_emb = nn.Embedding(num_embeddings=nmonth, embedding_dim=64)
        self.date_emb = nn.Embedding(num_embeddings=ndate, embedding_dim=64)
        self.season_emb = nn.Embedding(num_embeddings=nseason, embedding_dim=64)
        self.inflow_layer = nn.Sequential(
            nn.Linear(in_features=2, out_features=8),
            nn.SELU(),
            nn.Linear(in_features=8, out_features=16),
            nn.BatchNorm1d(16),
            nn.SELU()
        )
        
        self.outflow_layer = nn.Sequential(
            nn.Linear(in_features=64*3+16, out_features=64),
            nn.SELU(),
            nn.Linear(in_features=64, out_features=16),
            nn.SELU(),
            nn.Linear(in_features=16, out_features=1),
            nn.ReLU()
        )
    
    def forward(self, x_month, x_date, x_season, x_inflow):
        bs = x_month.shape[0]

        month_out = self.month_emb(x_month)
        date_out = self.date_emb(x_date)
        season_out = self.season_emb(x_season)
        inflow_out = self.inflow_layer(x_inflow)

        x = torch.cat([month_out, date_out, season_out, inflow_out], axis=-1)
        outflow = self.outflow_layer(x)

        return outflow.view(bs)