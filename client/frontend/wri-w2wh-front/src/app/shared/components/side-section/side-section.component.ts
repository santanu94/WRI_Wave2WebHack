import { Component, OnInit } from '@angular/core';
import { ThemePalette } from '@angular/material/core';
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

  constructor(private sharedService: SharedService) { }

  ngOnInit(): void {
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
