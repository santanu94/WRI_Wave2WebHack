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
  public dataPopulationSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public dataPopulationObservable: Observable<any>;

  public cumulativeInflowArray: number[] = [];
  public inflowArray: number[] = [];
  public outflowArray: number[] = [];
  public storageArray: number[] = [];
  public durationArray: any[] = [];
  public datesArray: any[] = [];
  public seasonalOutflowAmcsArray: number[] = [];
  public seasonalOutflowNoAmcsArray: number[] = [];
  public seasonalLabelsArray: string[] = [];
  public dailyDisplaynSeasonalSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public dailyDisplaynSeasonalObservable: Observable<any>;

  moduleName = '/common';
  getServerUrl = () => environment.serverUrl + this.moduleName;

  constructor(private httpClient: HttpClient) {
    this.regionObservable = this.regionSubject.asObservable();
    this.yearObservable = this.yearSubject.asObservable();
    this.dataPopulationObservable = this.dataPopulationSubject.asObservable();
    this.dailyDisplaynSeasonalObservable = this.dailyDisplaynSeasonalSubject.asObservable();
  }

  getRegionList() {
    return this.httpClient.get(this.getServerUrl() + '/regionList');
  }

  getYearlist() {
    return this.httpClient.get(this.getServerUrl() + '/getYearlist');
  }

  getDailynSeasonalData() {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', this.selectedRegion);
    urlParams = urlParams.set('years', this.selectedYear);
    return this.httpClient.get(this.getServerUrl() + '/getDailynSeasonalData', {params: urlParams});
  }
}
