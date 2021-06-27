import { Component, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared/services/shared.service';

@Component({
  selector: 'app-prediction-base',
  templateUrl: './prediction-base.component.html',
  styleUrls: ['./prediction-base.component.css']
})
export class PredictionBaseComponent implements OnInit {

  public passedRegion: string;

  constructor(private sharedService: SharedService) { }

  ngOnInit(): void {
    this.passedRegion = this.sharedService.selectedRegion;
  }

}
