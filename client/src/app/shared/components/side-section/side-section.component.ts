import { Component, OnInit } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
import { AuthService } from 'src/app/login-register/services/auth.service';
import { SharedService } from '../../services/shared.service';

export interface RegionModel {
  regionName: string;
  color: ThemePalette;
  maxCapacity: number;
}

@Component({
  selector: 'app-side-section',
  templateUrl: './side-section.component.html',
  styleUrls: ['./side-section.component.css']
})
export class SideSectionComponent implements OnInit {

  regionList: RegionModel[] = [];

  zoom = 6;
  center: google.maps.LatLngLiteral;
  options: google.maps.MapOptions = {
    mapTypeId: 'roadmap',
    zoomControl: false,
    scrollwheel: false,
    disableDoubleClickZoom: false,
    maxZoom: 25,
    minZoom: 4
  };

  markers: any[] = [];
  coordinates: any[] = [];

  constructor(
    private sharedService: SharedService,
    public authService: AuthService
  ) { }

  ngOnInit(): void {

    this.center = {
      lat: 12.4255,
      lng: 76.5724
    };

    this.coordinates = [{
      lat: 12.3375,
      lng: 75.8069,
      loc: 'Kodagu'
    }, {
      lat: 12.2958,
      lng: 76.6394,
      loc: 'Mysuru'
    }, {
      lat: 13.0033,
      lng: 76.1004,
      loc: 'Hassan'
    }];

    this.setMarkers();

    this.sharedService.getRegionList().subscribe(
      (response: any) => {
        this.regionList = response.regionList;
        this.sharedService.selectedRegion = this.regionList[0].regionName;
        this.sharedService.maxCapacity = this.regionList[0].maxCapacity;
      },
      error => {
        this.regionList = [];
        console.log(error);
      }
    );
  }

  setMarkers() {
    this.coordinates.forEach(element => {
      this.markers.push({
        position: {
          lat: element.lat,
          lng: element.lng
        },
        label: {
          color: 'white',
          text: element.loc,
        },
        title: element.loc,
        options: { animation: google.maps.Animation.DROP },
      });
    });
  }

  zoomIn() {
    if (this.zoom < this.options.maxZoom) {
      this.zoom++;
    }
  }

  zoomOut() {
    if (this.zoom > this.options.minZoom) {
      this.zoom--;
    }
  }

  regionSelect(value: RegionModel) {
    this.sharedService.selectedRegion = value.regionName;
    this.sharedService.maxCapacity = value.maxCapacity;
    this.sharedService.regionSubject.next(true);
    this.sharedService.dataPopulationSubject.next(false);
    this.sharedService.dailyDisplaynSeasonalSubject.next(false);
    this.sharedService.dailyStatsLastValue = -1;
    this.sharedService.dateSelectSubject.next(false);
  }

}
