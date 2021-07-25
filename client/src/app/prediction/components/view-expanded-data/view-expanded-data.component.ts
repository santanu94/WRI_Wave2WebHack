import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, Label } from 'ng2-charts';

@Component({
  selector: 'app-view-expanded-data',
  templateUrl: './view-expanded-data.component.html',
  styleUrls: ['./view-expanded-data.component.css']
})
export class ViewExpandedDataComponent implements OnInit {

  chartData: ChartDataSets[] = [];
  chartLabels: Label[] = [];
  chartOptions: ChartOptions;
  chartColors: Color[] = [];
  chartLegend = true;
  chartPlugins = [];
  chartType: string;

  headerData: string;
  labelDetailsData: string;
  predictedDataSetLabel: string;
  actualAmcsDataSetLabel: string;
  outflowArrayDataSetLabel: string;

  constructor(
    @Inject(MAT_DIALOG_DATA) public dialogData,
    public dialogRef: MatDialogRef<ViewExpandedDataComponent>
  ) { }

  ngOnInit(): void {
    if (this.dialogData.data === 'INFLOW') {
      this.headerData = 'Inflow Current Cycle';
      this.actualAmcsDataSetLabel = 'Actual Inflow Current Cycle';
      this.predictedDataSetLabel = 'Predicted Inflow';
    } else {
      this.headerData = 'Outflow Current Cycle';
      this.actualAmcsDataSetLabel = 'AMCS Outflow Current Cycle';
      this.predictedDataSetLabel = 'Actual Outflow';
      this.outflowArrayDataSetLabel = 'Outflow';
    }
    const years = this.dialogData.yearDetails.split(' - ');
    this.labelDetailsData = 'Days (June ' + years[0] + ' - ' + 'May ' + years[1] + ')';
    this.chartType = 'line';
    this.chartLabels = this.getChartLabels();
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        xAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: this.labelDetailsData,
              fontSize: 20
            }
          }
        ],
        yAxes: [
          {
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Quantity (in cubic metres)',
              fontSize: 20
            }
          }
        ],
      }
    };
    if (this.dialogData.data === 'INFLOW') {
      this.chartData = [
        { data: this.dialogData.yearPredictedData, label: this.predictedDataSetLabel },
        { data: this.dialogData.yearActualAmcsData, label: this.actualAmcsDataSetLabel }
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
    } else {
      this.chartData = [
        { data: this.dialogData.yearPredictedData, label: this.predictedDataSetLabel },
        { data: this.dialogData.yearActualAmcsData, label: this.actualAmcsDataSetLabel },
        { data: this.dialogData.outflowfullYearData, label: this.outflowArrayDataSetLabel, hidden: true }
      ];
      this.chartColors = [
        {
          borderColor: 'black',
          backgroundColor: 'rgba(0,0,255,0.28)',
        },
        {
          borderColor: 'black',
          backgroundColor: 'rgba(0,255,0,0.28)',
        },
        {
          borderColor: 'black',
          backgroundColor: 'rgba(255,69,0,0.5)',
        }
      ];
    }
  }

  closeDialog(){
    this.dialogRef.close();
  }

  getChartLabels(): string[] {
    const returnArray = [];
    for (let i = 1; i <= this.dialogData.yearPredictedData.length; i++) {
      returnArray.push(i.toString());
    }
    return returnArray;
  }

}
