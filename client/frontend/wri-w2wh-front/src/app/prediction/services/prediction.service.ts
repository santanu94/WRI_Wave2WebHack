import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {

  public displayMonths = ['June', 'July', 'August', 'September', 'October', 'November', 'December',
           'January', 'February', 'March', 'April', 'May'];

  public inflowDataSet: number[] = [];
  public outflowDataSet: number[] = [];

  moduleName = '/prediction';
  getServerUrl = () => environment.serverUrl + this.moduleName;

  constructor(private httpClient: HttpClient) {}

  getAllArrayData(region: string, year: string) {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', region);
    urlParams = urlParams.set('years', year);
    return this.httpClient.get(this.getServerUrl() + '/getInflowOutflowArrayData', {params: urlParams});
  }

  getExpandedData(region: string, year: string, typeOfData: string) {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', region);
    urlParams = urlParams.set('years', year);
    urlParams = urlParams.set('typeOfData', typeOfData);
    return this.httpClient.get(this.getServerUrl() + '/getExpandedData', {params: urlParams});
  }

  getTrendsData(region: string, year: string) {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', region);
    urlParams = urlParams.set('year', year);
    return this.httpClient.get(this.getServerUrl() + '/getInflowTrends', {params: urlParams});
  }
}
