import { Component, Input, OnInit } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { SharedService } from 'src/app/shared/services/shared.service';
import { PredictionService } from '../../services/prediction.service';
import { ViewExpandedDataComponent } from '../view-expanded-data/view-expanded-data.component';

@Component({
  selector: 'app-inflow-current-cycle',
  templateUrl: './inflow-current-cycle.component.html',
  styleUrls: ['./inflow-current-cycle.component.css']
})
export class InflowCurrentCycleComponent implements OnInit {

  chartData: ChartDataSets[] = [];
  chartLabels: Label[] = [];
  chartOptions: ChartOptions;
  chartColors: Color[] = [];
  chartLegend = true;
  chartPlugins = [];
  chartType: string;
  @Input() showExpand: boolean;

  constructor(
    private predictionService: PredictionService,
    private sharedService: SharedService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.chartType = 'line';
    this.chartLabels = this.predictionService.displayMonths;
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false
    };
    this.chartData = [
      { data: [], label: 'Predicted Inflow' },
      { data: [], label: 'Actual Inflow' }
    ];
    this.chartColors = [
      {
        borderColor: 'black',
        backgroundColor: 'rgba(0,0,255,0.28)',
      },
      {
        borderColor: 'black',
        backgroundColor: 'rgba(0,255,0,0.28)',
      }
    ];
    this.sharedService.dataPopulationObservable.subscribe(
      (dataPopulated) => {
        if (dataPopulated) {
          this.chartData = [
            { data: this.predictionService.inflowDataSet, label: 'Predicted Inflow' },
            { data: this.predictionService.actualInflowDataSet, label: 'Actual Inflow' }
          ];
        }
      }
    );
  }

  onExpandClick(typeOfData: string) {
    const config = new MatDialogConfig();
    config.width = '150%';
    config.autoFocus = true;
    config.disableClose = true;
    config.hasBackdrop = true;
    this.predictionService.getExpandedData(this.sharedService.selectedRegion,
      this.sharedService.selectedYear.toString(), typeOfData)
      .subscribe((response: any) => {
        config.data = {
          yearPredictedData: response.predictedfullYearData,
          yearActualAmcsData: response.actual_amcsfullYearData,
          yearDetails: this.sharedService.selectedYear,
          data: typeOfData
        };
        this.dialog.open(ViewExpandedDataComponent, config);
    });
  }

}
