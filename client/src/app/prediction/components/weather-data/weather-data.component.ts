import { Component, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { MatExpansionPanel } from '@angular/material/expansion';
import { SharedService } from 'src/app/shared/services/shared.service';

@Component({
  selector: 'app-weather-data',
  templateUrl: './weather-data.component.html',
  styleUrls: ['./weather-data.component.css']
})
export class WeatherDataComponent implements OnInit {

  regionList: any[] = [];
  timeframeList: any[] = [];
  timeframeIndex: any[] = [];
  weatherDataList: any[] = [];
  timeframeDetails = null;
  panelOpenState = false;
  loadingData = false;
  selectedWeatherRegion = 'Kodagu';

  dateData: any = null;
  @Output() openEvent = new EventEmitter<any>();
  @Output() closeEvent = new EventEmitter<any>();
  @Output() nextDayEvent = new EventEmitter<any>();
  @Output() prevDayEvent = new EventEmitter<any>();

  @ViewChild('expansionPanel', {static: true}) matExpansionPanelElement: MatExpansionPanel;

  constructor(public sharedService: SharedService) {
    sharedService.getWeatherRegionList().subscribe(
      (response: any) => { this.regionList = response.regionList; });
  }

  ngOnInit(): void {
    for (let i = 0; i < 24; i += 4) {
      this.timeframeList.push(i < 10 ? '0' + i.toString() + ':00:00' : i.toString() + ':00:00');
      this.timeframeIndex.push(i);
    }
    this.timeframeList.push('23:00:00');
    this.timeframeIndex.push(23);
    this.sharedService.yearObservable.subscribe(data => {
      if (data) {
        this.matExpansionPanelElement.close();
      }
    });
    this.sharedService.regionObservable.subscribe(data => {
      if (data) {
        this.matExpansionPanelElement.close();
      }
    });
    this.sharedService.dateSelectObservable.subscribe(data => {
      if (data) {
        if (this.matExpansionPanelElement.expanded) {
          this.onOpen();
        } else {
          this.matExpansionPanelElement.open();
        }
      }
    });
  }

  onRegionSelect(value: string) {
    this.selectedWeatherRegion = value;
    this.loadingData = true;
    this.fetchDataMethod();
  }

  onOpen() {
    this.panelOpenState = true;
    this.openEvent.emit();
    this.loadingData = true;
    const stoppingDate = this.sharedService.datesArray[this.sharedService.dailyStatsLastValue + 1].split('-');
    this.dateData = new Date(+stoppingDate[2], +stoppingDate[1] - 1, +stoppingDate[0]).toISOString().slice(0, 10);
    this.fetchDataMethod();
    this.sharedService.weatherOpenForP2WSubject.next(true);
  }

  fetchDataMethod() {
    this.timeframeDetails = null;
    if (!!this.dateData) {
      this.sharedService.getWeatherData(this.selectedWeatherRegion, this.dateData).subscribe(
        (response: any) => {
          this.loadingData = false;
          this.weatherDataList = response.weather;
          this.timeframeDetails = !!this.weatherDataList ? this.weatherDataList[0] : null;
          this.timeframeDetails.hourNumber = this.timeframeList[0];
      });
    }
  }

  selectionChange(event: any) {
    this.timeframeDetails = !!this.weatherDataList ? this.weatherDataList[this.timeframeIndex[event.selectedIndex]] : null;
    this.timeframeDetails.hourNumber = this.timeframeList[event.selectedIndex];
  }

  onClose() {
    this.weatherDataList = [];
    this.timeframeDetails = null;
    this.panelOpenState = false;
    this.closeEvent.emit();
    this.sharedService.weatherOpenForP2WSubject.next(false);
  }

  prevDayClick() {
    this.sharedService.dailyStatsLastValue--;
    const prevDayDate = this.sharedService.datesArray[this.sharedService.dailyStatsLastValue + 1].split('-');
    this.dateData = new Date(+prevDayDate[2], +prevDayDate[1] - 1, +prevDayDate[0]).toISOString().slice(0, 10);
    this.prevDayEvent.emit();
    this.loadingData = true;
    this.fetchDataMethod();
  }

  nextDayClick() {
    this.sharedService.dailyStatsLastValue++;
    const nextDayDate = this.sharedService.datesArray[this.sharedService.dailyStatsLastValue + 1].split('-');
    this.dateData = new Date(+nextDayDate[2], +nextDayDate[1] - 1, +nextDayDate[0]).toISOString().slice(0, 10);
    this.nextDayEvent.emit();
    this.loadingData = true;
    this.fetchDataMethod();
  }

}
