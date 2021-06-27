import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  public selectedRegion: string;
  public regionSubject: BehaviorSubject<any> = new BehaviorSubject(false);
  public regionObservable: Observable<any>;
  moduleName = '/common';
  getServerUrl = () => environment.serverUrl + this.moduleName;

  constructor(private httpClient: HttpClient) {
    this.regionObservable = this.regionSubject.asObservable();
  }

  getStoragePercent() {
    return this.httpClient.get(this.getServerUrl() + '/storagePercent');
  }

  getRegionList() {
    return this.httpClient.get(this.getServerUrl() + '/regionList');
  }
}
