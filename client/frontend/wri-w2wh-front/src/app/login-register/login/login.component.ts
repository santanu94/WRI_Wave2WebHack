import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  signinupform: FormGroup;
  emailPattern = '^[a-zA-Z0-9.!#$%&*+/=?^_{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$';
  passwordPattern = '^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$';

  constructor(
    public authService: AuthService
  ) { }

  get signinupFormValues() {
    return this.signinupform.controls;
  }

  ngOnInit(): void {
    this.signinupform = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.pattern(this.emailPattern)]),
      password: new FormControl('', [Validators.required, Validators.pattern(this.passwordPattern)])
    });
  }

  signInUpMethod(type: string) {
    this.authService.disableFlag = true;
    this.signinupFormValues.email.markAllAsTouched();
    this.signinupFormValues.password.markAllAsTouched();
    if (!this.signinupFormValues.email.invalid && !this.signinupFormValues.password.invalid) {
      if (type === 'SIGNIN') {
        this.authService.SignIn(
          this.signinupFormValues.email.value.toString(),
          this.signinupFormValues.password.value.toString()
        );
      } else {
        this.authService.SignUp(
          this.signinupFormValues.email.value.toString(),
          this.signinupFormValues.password.value.toString()
        );
      }
    }
  }

}
