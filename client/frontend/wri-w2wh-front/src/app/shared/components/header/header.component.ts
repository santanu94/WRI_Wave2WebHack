import { Component, OnInit } from '@angular/core';
import { SharedService } from '../../services/shared.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  yearList: string[] = [];

  constructor(
    public sharedService: SharedService
  ) { }

  ngOnInit(): void {
    this.sharedService.getYearlist().subscribe(
      (response: any) => {
        this.yearList = response.yearlist;
      }
    );
  }

  onYearChange() {
    this.sharedService.yearSubject.next(true);
    this.sharedService.dataPopulationSubject.next(false);
  }

}
