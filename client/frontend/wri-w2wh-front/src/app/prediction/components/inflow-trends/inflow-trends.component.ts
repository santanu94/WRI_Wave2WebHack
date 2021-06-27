import { Component, Input, OnInit } from '@angular/core';
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
  @Input() passedRegion: string;

  constructor(
    private predictionService: PredictionService,
    private sharedService: SharedService
  ) { }

  ngOnInit(): void {
    this.chartType = 'line';
    this.chartLabels = this.predictionService.displayMonths;
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false
    };

    this.chartColors = [
      {
        borderColor: 'black',
        backgroundColor: 'rgba(0,0,255,0.28)',
      }
    ];
    this.fetchDataBasedOnRegion(this.passedRegion);
    this.sharedService.regionObservable.subscribe(
      (changeTrigger) => {
        if (changeTrigger) {
          this.fetchDataBasedOnRegion(this.sharedService.selectedRegion);
        }
      }
    );
  }

  fetchDataBasedOnRegion(region: string) {
    this.predictionService.getInflowTrendsData(region)
      .subscribe((response: {inflowTrendsArray: number[]}) => {
        if (!!response) {
          this.chartData = [
            { data: response.inflowTrendsArray, label: 'Rainfall' }
          ];
        } else {
          this.chartData = [
            { data: [], label: 'Rainfall' }
          ];
        }
      },
      error => {
        this.chartData = [
          { data: [], label: 'Rainfall' }
        ];
        console.log(error);
    });
  }

}
