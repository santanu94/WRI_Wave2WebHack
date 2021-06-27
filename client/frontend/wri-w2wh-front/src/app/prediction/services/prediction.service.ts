import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {

  public displayMonths = ['January', 'February', 'March', 'April', 'May', 'June',
         'July', 'August', 'September', 'October', 'November', 'December'];

  moduleName = '/prediction';
  getServerUrl = () => environment.serverUrl + this.moduleName;

  constructor(private httpClient: HttpClient) { }

  getInflowCurrentCycleData(region: string) {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', region);
    return this.httpClient.get(this.getServerUrl() + '/inflowCurrentCycle', {params: urlParams});
  }

  getOutflowData(region: string) {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', region);
    return this.httpClient.get(this.getServerUrl() + '/outflow', {params: urlParams});
  }

  getInflowTrendsData(region: string) {
    let urlParams = new HttpParams();
    urlParams = urlParams.set('region', region);
    return this.httpClient.get(this.getServerUrl() + '/inflowTrends', {params: urlParams});
  }
}
