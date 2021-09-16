import { Component, OnInit, ViewChild } from '@angular/core';
import { AuthService } from 'src/app/login-register/services/auth.service';
import { SharedService } from '../../services/shared.service';
import { MAT_DATE_FORMATS } from '@angular/material/core';
import { MatInput } from '@angular/material/input';
import * as moment from 'moment';

export const MY_DATE_FORMATS = {
  parse: {
    dateInput: 'YYYY-MM-DD',
  },
  display: {
    dateInput: 'MMM DD, YYYY',
    monthYearLabel: 'MMMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY'
  },
};

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
  providers: [
    { provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS }
  ]
})
export class HeaderComponent implements OnInit {

  yearList: string[] = [];
  minDate: any;
  maxDate: any;

  @ViewChild('dateInput', { read: MatInput }) public dateInput: MatInput;

  constructor(
    public sharedService: SharedService,
    public authService: AuthService
  ) { }

  ngOnInit(): void {
    this.sharedService.getYearlist().subscribe(
      (response: any) => {
        this.yearList = response.yearlist;
        this.minDate = new Date(+this.sharedService.selectedYear.split(' - ')[0], 5, 1);
        this.maxDate = new Date(+this.sharedService.selectedYear.split(' - ')[1], 4, 31);
      }
    );
    this.sharedService.regionObservable.subscribe(data => {
      if (data) {
        this.dateInput.value = '';
        this.sharedService.dateSelectSubject.next(false);
      }
    });
    this.sharedService.dailyDisplaynSeasonalObservable.subscribe(data => {
      if (data) {
        this.dateInput.value = '';
        this.sharedService.dateSelectSubject.next(false);
      }
    });
  }

  onYearChange() {
    this.sharedService.yearSubject.next(true);
    this.sharedService.dataPopulationSubject.next(false);
    this.sharedService.dailyDisplaynSeasonalSubject.next(false);
    this.sharedService.dailyStatsLastValue = -1;
    this.minDate = new Date(+this.sharedService.selectedYear.split(' - ')[0], 5, 1);
    this.maxDate = new Date(+this.sharedService.selectedYear.split(' - ')[1], 4, 31);
    this.sharedService.dateSelectSubject.next(false);
    this.dateInput.value = '';
  }

  onDateChange(event: any) {
    this.sharedService.dailyStatsLastValue = this.sharedService.datesArray.indexOf(
      event.value.date() + '-' + (event.value.month() + 1) + '-' + event.value.year());
    this.sharedService.dateSelectSubject.next(true);
  }

}
