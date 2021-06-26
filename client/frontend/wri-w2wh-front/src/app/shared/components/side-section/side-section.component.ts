import { Component, OnInit } from '@angular/core';
import { ThemePalette } from '@angular/material/core';

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

  storageGuageValue: string;
  regionList: RegionModel[] = [];

  constructor() { }

  ngOnInit(): void {
    this.storageGuageValue = '43';
    this.regionList = [
      {regionName: 'KRS', color: 'primary'},
      {regionName: 'KAB', color: 'primary'},
      {regionName: 'HEM', color: 'primary'},
      {regionName: 'HAR', color: 'primary'}
    ];
  }

}
