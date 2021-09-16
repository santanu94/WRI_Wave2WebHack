import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  public selectedRegion = 'KRS';
  public selectedYear = '2011 - 2012';
  public regionSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public regionObservable: Observable<any>;
  public yearSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public yearObservable: Observable<any>;
  public dateSelectSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public dateSelectObservable: Observable<any>;
  public dataPopulationSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public dataPopulationObservable: Observable<any>;

  public cumulativeInflowArray: number[] = [];
  public inflowArray: number[] = [];
  public outflowArray: number[] = [];
  public storageArray: number[] = [];
  public durationArray: any[] = [];
  public datesArray: any[] = [];

  public yearsPredictedvsActualData: any;
  public yearsPredictedvsNormalData: any;

  public dailyDisplaynSeasonalSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public dailyDisplaynSeasonalObservable: Observable<any>;

  public weatherOpenForP2WSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public weatherOpenForP2WObservable: Observable<any>;

  public borderColorArray: string[] = [];
  public backgroundColorArray: string[] = [];

  public dailyStatsLastValue = -1;
  public maxCapacity = 49.45;

  moduleName = '/common';
  getServerUrl = () => environment.serverUrl + this.moduleName;

  constructor(private httpClient: HttpClient) {
    this.regionObservable = this.regionSubject.asObservable();
    this.yearObservable = this.yearSubject.asObservable();
    this.dataPopulationObservable = this.dataPopulationSubject.asObservable();
    this.dailyDisplaynSeasonalObservable = this.dailyDisplaynSeasonalSubject.asObservable();
    this.dateSelectObservable = this.dateSelectSubject.asObservable();
    this.weatherOpenForP2WObservable = this.weatherOpenForP2WSubject.asObservable();
    this.populateColorsArray();
  }

  getRegionList() {
    return this.httpClient.get(this.getServerUrl() + '/regionList');
  }

  getWeatherRegionList() {
    return this.httpClient.get(this.getServerUrl() + '/weatherRegionList');
  }

  getYearlist() {
    return this.httpClient.get(this.getServerUrl() + '/getYearlist');
  }

  getcoordinatesList() {
    return this.httpClient.get(this.getServerUrl() + '/coordinatesList');
  }

  getDailynSeasonalData() {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', this.selectedRegion);
    urlParams = urlParams.set('years', this.selectedYear);
    return this.httpClient.get(this.getServerUrl() + '/getDailynSeasonalData', {params: urlParams});
  }

  getWeatherData(region: string, date: string) {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', region);
    urlParams = urlParams.set('date', date);
    return this.httpClient.get(this.getServerUrl() + '/getWeatherData', {params: urlParams});
  }

  populateColorsArray() {
    this.borderColorArray = [
      'rgba(0, 102, 255',
      'rgba(153, 51, 255',
      'rgba(255, 0, 255',
      'rgba(255, 51, 119',
      'rgba(255, 26, 26',
      'rgba(255, 209, 26',
      'rgba(0, 204, 0',
      'rgba(0, 204, 153',
      'rgba(255, 170, 0',
      'rgba(153, 0, 255'
    ];
    for (let i = 0; i < 10; i++) {
      this.backgroundColorArray.push(this.borderColorArray[i] + ', 0.5)');
      this.borderColorArray[i] += ')';
    }
  }
}
