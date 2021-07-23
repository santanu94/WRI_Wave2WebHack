import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { SharedService } from 'src/app/shared/services/shared.service';
import { PredictionService } from '../../services/prediction.service';

@Component({
  selector: 'app-bar-chart-part',
  templateUrl: './bar-chart-part.component.html',
  styleUrls: ['./bar-chart-part.component.css']
})
export class BarChartPartComponent implements OnInit {

  chartData: ChartDataSets[] = [];
  chartLabels: Label[] = [];
  chartOptions: ChartOptions;
  chartColors: Color[] = [];
  chartLegend = true;
  chartPlugins = [];
  chartType: string;

  constructor(
    public sharedService: SharedService,
    public predictionService: PredictionService
  ) { }

  ngOnInit(): void {
    this.chartType = 'bar';
    this.chartLabels = this.predictionService.displaySeasons;
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false
    };
    this.chartData = [
      { data: [], label: '' },
      { data: [], label: '' }
    ];
    this.chartColors = [
      {
        borderColor: 'rgba(255,153,0)',
        backgroundColor: 'rgba(255,153,0,0.5)',
      },
      {
        borderColor: 'rgba(0,0,255)',
        backgroundColor: 'rgba(0,0,255,0.5)',
      }
    ];

    this.sharedService.dailyDisplaynSeasonalObservable.subscribe(
      (dataReceived) => {
        if (dataReceived) {
          this.chartData = [
            {
              data: this.sharedService.seasonalOutflowAmcsArray,
              label: this.sharedService.seasonalLabelsArray[0],
              borderWidth: 4
            },
            {
              data: this.sharedService.seasonalOutflowNoAmcsArray,
              label: this.sharedService.seasonalLabelsArray[1],
              borderWidth: 4
            }
          ];
        }
      }
    );
  }

}
