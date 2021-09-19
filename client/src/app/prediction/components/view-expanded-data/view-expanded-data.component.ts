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

  forecastDataSetLabel: string;

  constructor(
    @Inject(MAT_DIALOG_DATA) public dialogData,
    public dialogRef: MatDialogRef<ViewExpandedDataComponent>
  ) { }

  ngOnInit(): void {
    this.chartType = 'line';
    this.chartLabels = this.getChartLabels();
    if (this.dialogData.expandedSection) {
      if (this.dialogData.data === 'INFLOW') {
        this.headerData = 'Inflow Current Cycle';
        this.actualAmcsDataSetLabel = 'Actual Inflow Current Cycle';
        this.predictedDataSetLabel = 'Predicted Inflow';
        this.chartData = [
          { data: this.dialogData.yearPredictedData, label: this.predictedDataSetLabel, lineTension: 0.1 },
          { data: this.dialogData.yearActualAmcsData, label: this.actualAmcsDataSetLabel, lineTension: 0.1 }
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
        this.headerData = 'Outflow Current Cycle';
        this.actualAmcsDataSetLabel = 'AMCS Outflow Current Cycle';
        this.predictedDataSetLabel = 'Actual Outflow';
        this.outflowArrayDataSetLabel = 'Outflow';
        this.chartData = [
          { data: this.dialogData.yearPredictedData, label: this.predictedDataSetLabel, lineTension: 0.1 },
          { data: this.dialogData.yearActualAmcsData, label: this.actualAmcsDataSetLabel, lineTension: 0.1 },
          { data: this.dialogData.outflowfullYearData, label: this.outflowArrayDataSetLabel, lineTension: 0.1, hidden: true }
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
      const years = this.dialogData.yearDetails.split(' - ');
      this.labelDetailsData = this.dialogData.fullYear ?
        'Days (June ' + years[0] + ' - ' + 'May ' + years[1] + ')' : 'Days starting from June 01,' + years[0];
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
    } else {
      if (this.dialogData.data === 'INFLOW') {
        this.headerData = 'Two Weeks Predicted Inflow';
        this.forecastDataSetLabel = 'Predicted Inflow';
      } else {
        this.headerData = 'Two Weeks Predicted Outflow';
        this.forecastDataSetLabel = 'Predicted Outflow';
      }
      this.chartData = [
        { data: this.dialogData.forecastDataArray, label: this.forecastDataSetLabel, lineTension: 0.1 },
      ];
      this.chartColors = [
        {
          borderColor: 'black',
          backgroundColor: 'rgba(0,0,255,0.28)',
        }
      ];
      this.chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              display: true,
              scaleLabel: {
                display: true,
                labelString: 'Dates next two weeks',
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
    }
  }

  closeDialog(){
    this.dialogRef.close();
  }

  getChartLabels(): string[] {
    const returnArray = [];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
      'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    if (this.dialogData.expandedSection) {
      for (let i = 1; i <= this.dialogData.yearPredictedData.length; i++) {
        returnArray.push(i.toString());
      }
    } else {
      this.dialogData.datesArray.forEach(element => {
        const dateValues = element.split('-');
        const dateElement = new Date(+dateValues[0], +dateValues[1] - 1, +dateValues[2]);
        returnArray.push(dateElement.getDate().toString() + ' ' + months[dateElement.getMonth()]
             + ', ' + dateElement.getFullYear().toString());
      });
    }
    return returnArray;
  }

}
