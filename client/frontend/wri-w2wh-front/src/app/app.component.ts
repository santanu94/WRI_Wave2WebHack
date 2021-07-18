import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SharedService } from './shared/services/shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'WRI_Wave2WebHack';
  public activeTab = 0;
  public cumulativeInflowDiff: number;

  constructor(
    private sharedService: SharedService,
    private router: Router
  ) {
    router.navigate(['prediction']);
  }

  ngOnInit(): void {
    this.sharedService.getCumulativeInflowDiff().subscribe(
      (response: any) => {
        this.cumulativeInflowDiff = response.cumulativeInflowDiff;
      },
      error => {
        this.cumulativeInflowDiff = 0;
        console.log(error);
      }
    );
  }

  moveToTab(event: any) {
    this.activeTab = event;
    this.router.navigate(this.activeTab ? ['amcs'] : ['prediction']);
  }
}
