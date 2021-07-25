import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { LoginRegisterRoutingModule } from './login-register-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    LoginComponent
  ],
  imports: [
    CommonModule,
    LoginRegisterRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class LoginRegisterModule { }
