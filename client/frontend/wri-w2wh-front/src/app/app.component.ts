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

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
    this.router.navigate(['prediction']);
  }

}
