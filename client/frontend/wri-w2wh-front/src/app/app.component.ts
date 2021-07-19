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
  public cumulativeInflowDiff: number;

  constructor(
    private sharedService: SharedService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.router.navigate(['prediction']);
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

}
