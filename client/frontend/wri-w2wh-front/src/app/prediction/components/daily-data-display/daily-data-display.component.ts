import { Component, OnInit } from '@angular/core';
import { interval } from 'rxjs';
import { take } from 'rxjs/operators';
import { SharedService } from 'src/app/shared/services/shared.service';

@Component({
  selector: 'app-daily-data-display',
  templateUrl: './daily-data-display.component.html',
  styleUrls: ['./daily-data-display.component.css']
})
export class DailyDataDisplayComponent implements OnInit {

  storageGuageValue: string;
  changetime = null;
  changetimeSubscribe = null;

  public cumulativeInflowDiff: number;
  public inflow: number;
  public outflow: number;
  public duration: any;
  public displayDate: any;
  public storage: any;

  constructor(public sharedService: SharedService) { }

  ngOnInit(): void {
    this.sharedService.dailyDisplaynSeasonalObservable.subscribe(
      (dataReceived) => {
        if (dataReceived) {
          this.changetime = interval(2000);
          this.changetime.pipe(take(this.sharedService.durationArray.length));
          this.changetimeSubscribe = this.changetime.subscribe(value => {
            if (this.sharedService.selectedYear === '2011 - 2012') {
              this.cumulativeInflowDiff = 0;
            } else {
              this.cumulativeInflowDiff = this.sharedService.cumulativeInflowArray[value];
            }
            this.inflow = this.sharedService.inflowArray[value];
            this.outflow = this.sharedService.outflowArray[value];
            if (this.sharedService.storageArray[value] < 100) {
              this.storage = this.sharedService.storageArray[value];
              this.storageGuageValue = this.storage.toString();
            } else {
              this.storage = this.storageGuageValue = this.sharedService.storageArray[value].toFixed(1);
            }
            this.duration = this.sharedService.durationArray[value];
            const nextDate = this.sharedService.datesArray[value].split('-');
            this.displayDate = new Date(+nextDate[2], +nextDate[1] - 1, +nextDate[0]);
          });
        } else {
          !!this.changetimeSubscribe ? this.changetimeSubscribe.unsubscribe() : this.changetimeSubscribe = null;
          this.changetime = null;
        }
      }
    );
  }

}
