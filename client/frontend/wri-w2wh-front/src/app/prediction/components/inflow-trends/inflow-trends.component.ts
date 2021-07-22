import { Component, OnInit } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { SharedService } from 'src/app/shared/services/shared.service';
import { PredictionService } from '../../services/prediction.service';

@Component({
  selector: 'app-inflow-trends',
  templateUrl: './inflow-trends.component.html',
  styleUrls: ['./inflow-trends.component.css']
})
export class InflowTrendsComponent implements OnInit {

  chartData: ChartDataSets[] = [];
  chartLabels: Label[] = [];
  chartOptions: ChartOptions;
  chartColors: Color[] = [];
  chartLegend = true;
  chartPlugins = [];
  chartType: string;

  noTrendsGraph = true;
  trendsValue = 0;

  constructor(
    private predictionService: PredictionService,
    private sharedService: SharedService
  ) { }

  ngOnInit(): void {
    this.chartType = 'line';
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false
    };
    this.chartData = [
      { data: [], label: 'Rainfall' }
    ];
    this.chartColors = [
      {
        borderColor: 'black',
        backgroundColor: 'rgba(0,0,255,0.28)',
      }
    ];

    if (this.sharedService.selectedYear.indexOf('2011') !== -1) {
      this.noTrendsGraph = true;
      this.trendsValue = 0;
    }

    this.sharedService.dataPopulationObservable.subscribe(
      (dataPopulated) => {
        if (dataPopulated) {
          if (this.sharedService.selectedYear.indexOf('2011') !== -1) {
            this.noTrendsGraph = true;
            this.trendsValue = 0;
            this.sharedService.getDailynSeasonalData().subscribe(
              (cResponse: any) => {
                this.sharedService.cumulativeInflowArray = cResponse.cumulativeInflowDiff;
                this.sharedService.inflowArray = cResponse.inflowArray;
                this.sharedService.outflowArray = cResponse.outflowArray;
                this.sharedService.storageArray = cResponse.storageArray;
                this.sharedService.durationArray = cResponse.durationArray;
                this.sharedService.datesArray = cResponse.datesArray;
                this.sharedService.seasonalOutflowAmcsArray = cResponse.seasonalOutflowAmcsArray;
                this.sharedService.seasonalOutflowNoAmcsArray = cResponse.seasonalOutflowNoAmcsArray;
                this.sharedService.seasonalLabelsArray = cResponse.seasonalLabelsArray;
                this.sharedService.dailyDisplaynSeasonalSubject.next(true);
              },
              error => {
                this.sharedService.cumulativeInflowArray = [];
                this.sharedService.inflowArray = [];
                this.sharedService.outflowArray = [];
                this.sharedService.storageArray = [];
                this.sharedService.durationArray = [];
                this.sharedService.datesArray = [];
                console.log(error);
              }
            );
          } else {
            this.predictionService.getTrendsData(this.sharedService.selectedRegion, this.sharedService.selectedYear).subscribe(
              (response: any) => {
                if (!!response.noOfValues && response.noOfValues === 1) {
                  this.noTrendsGraph = true;
                  this.trendsValue = response.trendsValue;
                } else {
                  this.noTrendsGraph = false;
                  this.chartLabels = response.trendsLabel;
                  this.chartData = [
                    { data: response.trendsArray, label: 'Rainfall' }
                  ];
                }
                this.sharedService.getDailynSeasonalData().subscribe(
                  (cResponse: any) => {
                    this.sharedService.cumulativeInflowArray = cResponse.cumulativeInflowDiff;
                    this.sharedService.inflowArray = cResponse.inflowArray;
                    this.sharedService.outflowArray = cResponse.outflowArray;
                    this.sharedService.storageArray = cResponse.storageArray;
                    this.sharedService.durationArray = cResponse.durationArray;
                    this.sharedService.datesArray = cResponse.datesArray;
                    this.sharedService.seasonalOutflowAmcsArray = cResponse.seasonalOutflowAmcsArray;
                    this.sharedService.seasonalOutflowNoAmcsArray = cResponse.seasonalOutflowNoAmcsArray;
                    this.sharedService.seasonalLabelsArray = cResponse.seasonalLabelsArray;
                    this.sharedService.dailyDisplaynSeasonalSubject.next(true);
                  },
                  error => {
                    this.sharedService.cumulativeInflowArray = [];
                    this.sharedService.inflowArray = [];
                    this.sharedService.outflowArray = [];
                    this.sharedService.storageArray = [];
                    this.sharedService.durationArray = [];
                    this.sharedService.datesArray = [];
                    console.log(error);
                  }
                );
              },
              error => {
                this.chartData = [{ data: [], label: 'Rainfall' }];
                this.chartLabels = [];
                console.log(error);
            });
          }
        }
    });
  }

}
