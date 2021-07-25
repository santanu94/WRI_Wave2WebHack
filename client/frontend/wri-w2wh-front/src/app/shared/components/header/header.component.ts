import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/login-register/services/auth.service';
import { SharedService } from '../../services/shared.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  yearList: string[] = [];

  constructor(
    public sharedService: SharedService,
    public authService: AuthService
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
    this.sharedService.dailyDisplaynSeasonalSubject.next(false);
  }

}
