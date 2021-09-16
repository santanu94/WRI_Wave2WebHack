import { Component, OnInit } from '@angular/core';
import { interval, Observable, of, range } from 'rxjs';
import { concatMap, delay, take } from 'rxjs/operators';
import { SharedService } from 'src/app/shared/services/shared.service';

@Component({
  selector: 'app-daily-data-display',
  templateUrl: './daily-data-display.component.html',
  styleUrls: ['./daily-data-display.component.css']
})
export class DailyDataDisplayComponent implements OnInit {

  storageGuageValue: string;
  changetime: Observable<number> = null;
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
          this.setObservables();
          this.changetimeSubscribe = this.changetime.subscribe(value => {
            this.sharedService.dailyStatsLastValue = value;
            this.setAllValues(value);
          });
        } else {
          !!this.changetimeSubscribe ? this.changetimeSubscribe.unsubscribe() : this.changetimeSubscribe = null;
          this.changetime = null;
        }
      }
    );
  }

  setAllValues(arrIndex) {
    if (this.sharedService.selectedYear === '2011 - 2012') {
      this.cumulativeInflowDiff = 0;
    } else {
      this.cumulativeInflowDiff = this.sharedService.cumulativeInflowArray[arrIndex];
    }
    this.inflow = this.sharedService.inflowArray[arrIndex];
    this.outflow = this.sharedService.outflowArray[arrIndex];
    if (this.sharedService.storageArray[arrIndex] < 100) {
      this.storage = this.sharedService.storageArray[arrIndex];
    } else {
      this.storage = this.sharedService.storageArray[arrIndex].toFixed(1);
    }
    this.storageGuageValue = (this.storage / this.sharedService.maxCapacity * 100).toString();
    this.duration = this.sharedService.durationArray[arrIndex];
    const nextDate = this.sharedService.datesArray[arrIndex].split('-');
    this.displayDate = new Date(+nextDate[2], +nextDate[1] - 1, +nextDate[0]);
  }

  setObservables() {
    if (this.sharedService.dailyStatsLastValue !== -1) {
      this.changetime = range(this.sharedService.dailyStatsLastValue + 1,
        this.sharedService.durationArray.length - this.sharedService.dailyStatsLastValue - 1)
        .pipe(
          concatMap(emitVal => of(emitVal).pipe(delay(2000)))
        );
    } else {
      this.changetime = interval(2000).pipe(take(this.sharedService.durationArray.length - 1));
    }
  }

}
