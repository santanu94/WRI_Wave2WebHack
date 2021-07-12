import torch
import torch.nn as nn

class KRSInflowModel(nn.Module):
    def __init__(self, nmonth, ndate, nseason):
        super().__init__()
        self.month_emb = nn.Embedding(num_embeddings=nmonth, embedding_dim=32)
        self.date_emb = nn.Embedding(num_embeddings=ndate, embedding_dim=32)
        self.season_emb = nn.Embedding(num_embeddings=nseason, embedding_dim=32)
        self.prev_data_layer = nn.Sequential(
            nn.Linear(in_features=2, out_features=16),
            nn.SELU(),
            nn.Linear(in_features=16, out_features=32),
            nn.SELU()
        )

        self.conv_1 = nn.Conv2d(in_channels=6, out_channels=12, kernel_size=3, stride=1, padding=1)
        self.res_layer_1 = nn.Sequential(
            nn.BatchNorm2d(num_features=12),
            nn.SELU(),
            nn.Conv2d(in_channels=12, out_channels=12, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(num_features=12),
            nn.SELU(),
            nn.Conv2d(in_channels=12, out_channels=12, kernel_size=3, stride=1, padding=1)
        )
        self.hidden_layer_1 = nn.Sequential(
            nn.Conv2d(in_channels=12, out_channels=6, kernel_size=3, stride=2, padding=1),
            nn.LeakyReLU()
        )
        self.res_layer_2 = nn.Sequential(
            nn.BatchNorm2d(num_features=6),
            nn.SELU(),
            nn.Conv2d(in_channels=6, out_channels=6, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(num_features=6),
            nn.SELU(),
            nn.Conv2d(in_channels=6, out_channels=6, kernel_size=3, stride=1, padding=1)
        )
        self.hidden_layer_2 = nn.Sequential(
            nn.Conv2d(in_channels=6, out_channels=1, kernel_size=3, stride=2, padding=1),
            nn.SELU()
        )
        
        self.inflow_layer = nn.Sequential(
            nn.Linear(in_features=64, out_features=32),
            nn.SELU(),
            nn.Linear(in_features=32, out_features=1),
            nn.ReLU()
        )
    
    def forward(self, x_month, x_date, x_season, x_prev_data):
        bs = x_month.shape[0]

        month_out = self.month_emb(x_month)
        date_out = self.date_emb(x_date)
        season_out = self.season_emb(x_season)
        prev_data_out = self.prev_data_layer(x_prev_data)

        month_date = torch.bmm(month_out.view(bs, -1, 1), date_out.view(bs, 1, -1))
        month_season = torch.bmm(month_out.view(bs, -1, 1), season_out.view(bs, 1, -1))
        month_prev_data = torch.bmm(month_out.view(bs, -1, 1), prev_data_out.view(bs, 1, -1))
        date_season = torch.bmm(date_out.view(bs, -1, 1), season_out.view(bs, 1, -1))
        date_prev_date = torch.bmm(date_out.view(bs, -1, 1), prev_data_out.view(bs, 1, -1))
        season_prev_date = torch.bmm(season_out.view(bs, -1, 1), prev_data_out.view(bs, 1, -1))

        x = torch.stack([month_date, month_season, month_prev_data, date_season, date_prev_date, season_prev_date], axis=1)
        conv_out = self.conv_1(x)
        res_out_1 = self.res_layer_1(conv_out) + conv_out
        hidden_out_1 = self.hidden_layer_1(res_out_1)
        res_out_2 = self.res_layer_2(hidden_out_1) + hidden_out_1
        res_out_2 += hidden_out_1
        hidden_out_2 = self.hidden_layer_2(res_out_2)
        hidden_out_2 = hidden_out_2.view(bs, -1)
        
        inflow_out = self.inflow_layer(hidden_out_2)

        return inflow_out.view(bs)
    
    def weight_init(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.normal_(m.weight)
                nn.init.zeros_(m.bias)
            elif isinstance(m, nn.Embedding):
                nn.init.normal_(m.weight)