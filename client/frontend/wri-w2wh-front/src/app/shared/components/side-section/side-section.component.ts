import { Component, OnInit } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
import { AuthService } from 'src/app/login-register/services/auth.service';
import { SharedService } from '../../services/shared.service';

export interface RegionModel {
  regionName: string;
  color: ThemePalette;
}

@Component({
  selector: 'app-side-section',
  templateUrl: './side-section.component.html',
  styleUrls: ['./side-section.component.css']
})
export class SideSectionComponent implements OnInit {

  regionList: RegionModel[] = [];

  constructor(
    private sharedService: SharedService,
    public authService: AuthService
  ) { }

  ngOnInit(): void {
    console.log(this.authService.userData);
    this.sharedService.getRegionList().subscribe(
      (response: any) => {
        this.regionList = response.regionList;
        this.sharedService.selectedRegion = this.regionList[0].regionName;
      },
      error => {
        this.regionList = [];
        console.log(error);
      }
    );
  }

  regionSelect(value: string) {
    this.sharedService.selectedRegion = value;
    this.sharedService.regionSubject.next(true);
    this.sharedService.dataPopulationSubject.next(false);
    this.sharedService.dailyDisplaynSeasonalSubject.next(false);
  }

}
