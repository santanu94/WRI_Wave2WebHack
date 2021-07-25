import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './login-register/services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'The_Atlantians';

  constructor(
    public authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    if (this.authService.isLoggedIn) {
      this.router.navigate(['prediction']);
    }
  }

}
