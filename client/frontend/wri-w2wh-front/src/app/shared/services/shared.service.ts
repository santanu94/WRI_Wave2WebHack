import { HttpClient } from '@angular/common/http';
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

  moduleName = '/common';
  getServerUrl = () => environment.serverUrl + this.moduleName;

  constructor(private httpClient: HttpClient) {
    this.regionObservable = this.regionSubject.asObservable();
    this.yearObservable = this.yearSubject.asObservable();
    this.dataPopulationObservable = this.dataPopulationSubject.asObservable();
  }

  getStoragePercent() {
    return this.httpClient.get(this.getServerUrl() + '/storagePercent');
  }

  getRegionList() {
    return this.httpClient.get(this.getServerUrl() + '/regionList');
  }

  getYearlist() {
    return this.httpClient.get(this.getServerUrl() + '/getYearlist');
  }

  getCumulativeInflowDiff() {
    return this.httpClient.get(this.getServerUrl() + '/getCumulativeInflowDiff');
  }
}
