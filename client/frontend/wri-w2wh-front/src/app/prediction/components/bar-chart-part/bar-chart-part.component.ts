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

  chartDataActual: ChartDataSets[] = [];
  chartColorsActual: Color[] = [];

  chartDataNormal: ChartDataSets[] = [];
  chartColorsNormal: Color[] = [];

  chartLabels: Label[] = [];
  chartOptions: ChartOptions;
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
    this.sharedService.dailyDisplaynSeasonalObservable.subscribe(
      (dataReceived) => {
        if (dataReceived) {
          if (!!this.sharedService.yearsPredictedvsActualData && !!this.sharedService.yearsPredictedvsNormalData) {
            this.processDataForDisplay();
          }
        }
      }
    );
  }

  processDataForDisplay() {
    this.chartDataActual = [];
    this.chartColorsActual = [];
    this.chartDataNormal = [];
    this.chartColorsNormal = [];
    let index = 0;
    Object.keys(this.sharedService.yearsPredictedvsNormalData).forEach(key => {
      this.chartDataNormal.push(
        {
          data: Object.values(this.sharedService.yearsPredictedvsNormalData[key]) as number[],
          label: key
        }
      );
      this.chartColorsNormal.push(
        {
          borderColor: this.sharedService.borderColorArray[index],
          backgroundColor: this.sharedService.backgroundColorArray[index],
          borderWidth: 2
        }
      );
      index++;
    });
    index = 0;
    Object.keys(this.sharedService.yearsPredictedvsActualData).forEach(key => {
      this.chartDataActual.push(
        {
          data: Object.values(this.sharedService.yearsPredictedvsActualData[key]) as number[],
          label: key
        }
      );
      this.chartColorsActual.push(
        {
          borderColor: this.sharedService.borderColorArray[index],
          backgroundColor: this.sharedService.backgroundColorArray[index],
          borderWidth: 2
        }
      );
      index++;
    });
  }

}
