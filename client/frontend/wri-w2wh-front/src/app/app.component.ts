import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent{
  title = 'WRI_Wave2WebHack';
  activeTab = 0;

  constructor(private router: Router) {
    router.navigate(['prediction']);
  }

  moveToTab(event: any) {
    this.activeTab = event;
    this.router.navigate(this.activeTab ? ['amcs'] : ['prediction']);
  }
}
