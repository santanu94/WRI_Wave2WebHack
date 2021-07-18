import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators';
import { SharedService } from 'src/app/shared/services/shared.service';
import { PredictionService } from '../../services/prediction.service';

@Component({
  selector: 'app-prediction-base',
  templateUrl: './prediction-base.component.html',
  styleUrls: ['./prediction-base.component.css']
})
export class PredictionBaseComponent implements OnInit, OnDestroy {

  public notifier = new Subject();
  public showExpand = false;

  constructor(
    private predictionService: PredictionService,
    private sharedService: SharedService
  ) { }

  ngOnDestroy(): void {
    this.notifier.next();
    this.notifier.complete();
  }

  ngOnInit(): void {
    this.fetchAllData(this.sharedService.selectedRegion, this.sharedService.selectedYear);
    this.sharedService.regionObservable.subscribe(
      (changeTrigger) => {
        if (changeTrigger) {
          this.fetchAllData(this.sharedService.selectedRegion, this.sharedService.selectedYear);
        }
      }
    );
    this.sharedService.yearObservable.subscribe(
      (changeTrigger) => {
        if (changeTrigger) {
          this.fetchAllData(this.sharedService.selectedRegion, this.sharedService.selectedYear);
        }
      }
    );
  }

  fetchAllData(region: string, year: string) {
    this.showExpand = false;
    this.predictionService.getAllArrayData(region, year)
      .pipe(take(1), takeUntil(this.notifier))
      .subscribe((response: any) => {
        this.predictionService.inflowDataSet = response.inflowCurrentCycleArray;
        this.predictionService.outflowDataSet = response.outflowArray;
        this.sharedService.dataPopulationSubject.next(true);
        this.showExpand = true;
      },
      error => {
        this.predictionService.inflowDataSet = [];
        this.predictionService.outflowDataSet = [];
        console.log(error);
      });
  }

}

