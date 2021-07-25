import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './shared/services/auth.guard';


const routes: Routes = [
  { path: '', redirectTo: 'signinorup', pathMatch: 'full' },
  { path: 'prediction', canActivate: [AuthGuard],
    loadChildren: () =>
      import(
        './prediction/prediction.module'
      ).then((m) => m.PredictionModule)
  },
  { path: 'signinorup',
    loadChildren: () =>
      import(
        './login-register/login-register.module'
      ).then((m) => m.LoginRegisterModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
